# -*- coding: utf-8 -*-
import dill as pickle
from redis import Redis, WatchError
import signal
import time

_REDIS_CONN = None
_SHOULD_STOP = False
_IS_BUSY = False

JOB_TTL = 300
WORKER_TTL = 600

class StopException(Exception):
    pass

def worker_execute(func_pickled, arg):
    unpickled = pickle.loads(func_pickled)
    unpickled.__globals__["__builtins__"] = globals()["__builtins__"]
    return unpickled(arg)

def stop_worker(signum, frame):
    global _SHOULD_STOP

    _SHOULD_STOP = True

    # Raise an exception to exit immediately when the worker is idle
    # and blocked on the blpop call
    # 
    # If the worker is currently executing a job,
    # it will exit once the job is done
    if not _IS_BUSY:
        raise StopException()

def handle_dependent(job_id):
    job_key = 'jobs:{}'.format(job_id)

    # Does another job depend on this one?
    dependent = _REDIS_CONN.hget(job_key, 'dependent')
    if dependent is not None:
        dependent = dependent.decode()
        dependent_deps_key = 'jobs:{}:deps'.format(dependent)

        with _REDIS_CONN.pipeline() as pipe:
            while True:
                try:
                    pipe.watch(dependent_deps_key)
                    pipe.multi()
                    pipe.srem(dependent_deps_key, job_id)
                    pipe.scard(dependent_deps_key)
                    res = pipe.execute()
                    if res[-1] == 0:
                        # The job that just finished is the last dependency,
                        # so enqueue the dependent
                        _REDIS_CONN.hset('jobs:{}'.format(dependent), 'status', 'queued')
                        _REDIS_CONN.rpush('job_q', dependent)
                    break
                except WatchError:
                    continue

def worker_init(worker_id):
    global _REDIS_CONN
    global _IS_BUSY

    _REDIS_CONN = Redis()

    # Install signal handler
    signal.signal(signal.SIGINT, stop_worker)
    signal.signal(signal.SIGTERM, stop_worker)

    # Set worker state
    worker_key = 'workers:{}'.format(worker_id)
    _REDIS_CONN.hset(worker_key, 'state', 'idle')

    # Listen for jobs
    while not _SHOULD_STOP:
        try:
            # Keep this key only as long as the worker is alive
            _REDIS_CONN.expire(worker_key, WORKER_TTL)

            _IS_BUSY = False

            # Block until there is a job to do
            packed = _REDIS_CONN.blpop('job_q', WORKER_TTL - 15)
            if packed is None:
                continue

            _IS_BUSY = True

            # We've got a job to do
            job_id = packed[1].decode()
            job_key = 'jobs:{}'.format(job_id)

            # update this worker's state and current job
            _REDIS_CONN.hset(worker_key, 'current_job', job_id)
            _REDIS_CONN.hset(worker_key, 'state', 'busy')

            func_pickled = _REDIS_CONN.hget(job_key, 'func')
            job_type = _REDIS_CONN.hget(job_key, 'type')
            arg = None

            if job_type.decode() == 'map':
                arg = _REDIS_CONN.hget(job_key, 'arg').decode()
            else:
                # reduce job, since there are no other supported types
                dependencies = _REDIS_CONN.smembers('{}:dependencies'.format(job_key))
                # check that all dependencies executed successfully (no failures)
                if all(map(lambda x: _REDIS_CONN.hget('jobs:{}'.format(x.decode()), 'status').decode() == 'finished', dependencies)):
                    arg = list(map(lambda x: pickle.loads(_REDIS_CONN.hget('jobs:{}'.format(x.decode()), 'result')), dependencies))

            try:
                # if a dependency failed, mark job as failed
                if arg is None:
                    raise Exception()

                result = worker_execute(func_pickled, arg)

                # Mark job as finished
                _REDIS_CONN.hset(job_key, 'status', 'finished')

                # Store the result
                _REDIS_CONN.hset(job_key, 'result', pickle.dumps(result))
            except:
                # The job raised an exception: mark job as failed
                _REDIS_CONN.hset(job_key, 'status', 'failed')
                pass

            # Unix timestamp
            _REDIS_CONN.hset(job_key, 'ended_at', int(time.time()))

            handle_dependent(job_id)

            # Keep the job info and results for 5 minutes
            _REDIS_CONN.expire(job_key, JOB_TTL)
            _REDIS_CONN.expire('{}:dependencies'.format(job_key), JOB_TTL)

            # update this worker's state and current job
            _REDIS_CONN.hdel(worker_key, 'current_job')
            _REDIS_CONN.hset(worker_key, 'state', 'idle')
        except StopException:
            break

    # Quitting worker, so remove its key
    _REDIS_CONN.delete(worker_key)
