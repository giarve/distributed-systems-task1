# -*- coding: utf-8 -*-
from redis import Redis
from rq import Connection, Queue, Worker

import dill as pickle

_REDIS_QUEUE = None

def worker_execute(func_pickled, arg):
    unpickled = pickle.loads(func_pickled)
    unpickled.__globals__["__builtins__"] = globals()["__builtins__"]
    return unpickled(arg)

def worker_execute_reduce(func_pickled, job_list):
    unpickled = pickle.loads(func_pickled)
    unpickled.__globals__["__builtins__"] = globals()["__builtins__"]
    results = list(map(lambda x: _REDIS_QUEUE.fetch_job(x).result, job_list))
    return unpickled(results)

def worker_init(worker_id):
    global _REDIS_QUEUE

    with Connection():
        _REDIS_QUEUE = Queue()
        Worker(_REDIS_QUEUE, name="{}".format(worker_id)).work()
