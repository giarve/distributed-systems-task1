#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Task 1: High Performance Computing Cluster"""

from concurrent import futures
import logging
import multiprocessing
import dill as pickle
import sys
from uuid import uuid4

import grpc

import server_pb2
import server_pb2_grpc
from google.protobuf import timestamp_pb2

import worker as wk

from redis import Redis

_LOGGER = logging.getLogger(__name__)

_PROCESS_COUNT = multiprocessing.cpu_count()

_WORKER_ID = 0
_WORKERS = {}

_BIND_ADDRESS = 'localhost:12312'

_REDIS_CONN = None

class WorkerManagement(server_pb2_grpc.WorkerManagementServicer):

    def create(self, request, context):  
        global _WORKER_ID
        
        _LOGGER.info('Creating %d workers', request.num)

        for _ in range(request.num):
            worker = multiprocessing.Process(target=wk.worker_init, args=(_WORKER_ID,))
            worker.start()
            _WORKERS[_WORKER_ID] = worker
            _LOGGER.info('Creating a worker %s', worker)
            _WORKER_ID += 1

        return server_pb2.Status(ok=True)

    def list(self, request, context):
        result = []
        keys = _REDIS_CONN.keys("workers:*")
        for k in keys:
            k = k.decode()
            state = _REDIS_CONN.hget(k, 'state').decode()
            current_job = None
            if state == 'busy':
                current_job = _REDIS_CONN.hget(k, 'current_job').decode()

            w = server_pb2.WorkerInfo(id=int(k.partition(':')[2]), current_state=state, current_job=current_job)
            result.append(w)

        return server_pb2.WorkerList(workers=result)

    def delete(self, request, context):
        worker = _WORKERS.pop(request.id, None)
        if worker is None:
            return server_pb2.Status(ok=False)

        _LOGGER.info('Terminating the worker %s', request.id)
        # Send SIGTERM to the worker
        # it will exit immediately if it's idle or
        # after it finishes executing the current job
        worker.terminate()
        return server_pb2.Status(ok=True)


class JobManagement(server_pb2_grpc.JobManagementServicer):
    def create(self, request, context):
        arg_list = list(request.args)

        job_list = []

        if len(arg_list) > 1:
            job_id_reduce = uuid4().hex
            reduce_key = 'jobs:{}'.format(job_id_reduce)

            _REDIS_CONN.hset(reduce_key, 'status', 'deferred')
            _REDIS_CONN.hset(reduce_key, 'type', 'reduce')
            _REDIS_CONN.hset(reduce_key, 'func', request.reduce_function_pickled)

            for arg in arg_list:
                job_id = uuid4().hex
                job_list.append(job_id)
                job_key = 'jobs:{}'.format(job_id)
                _REDIS_CONN.hset(job_key, 'arg', arg)
                _REDIS_CONN.hset(job_key, 'dependent', job_id_reduce)
                _REDIS_CONN.hset(job_key, 'status', 'queued')
                _REDIS_CONN.hset(job_key, 'type', 'map')
                _REDIS_CONN.hset(job_key, 'func', request.map_function_pickled)
                # deps -> jobs still pending to execute before the reduce job can be queued
                # dependencies -> kept so the reduce job can retrieve the results from the map functions
                _REDIS_CONN.sadd('{}:deps'.format(reduce_key), job_id)
                _REDIS_CONN.sadd('{}:dependencies'.format(reduce_key), job_id)
                _REDIS_CONN.rpush('job_q', job_id)

            return server_pb2.JobId(id=job_id_reduce)
        else:
            arg = arg_list[0] if len(arg_list) > 0 else ''
            job_id = uuid4().hex
            job_key = 'jobs:{}'.format(job_id)
            _REDIS_CONN.hset(job_key, 'arg', arg)
            _REDIS_CONN.hset(job_key, 'status', 'queued')
            _REDIS_CONN.hset(job_key, 'type', 'map')
            _REDIS_CONN.hset(job_key, 'func', request.map_function_pickled)
            _REDIS_CONN.rpush('job_q', job_id)

            return server_pb2.JobId(id=job_id)

    def list(self, request, context):
        jobs = []
        keys = _REDIS_CONN.keys('jobs:' + '?' * 32)
        for k in keys:
            k = k.decode()
            status = _REDIS_CONN.hget(k, 'status').decode()
            result = None
            if status == 'finished':
                result = str(pickle.loads(_REDIS_CONN.hget(k, 'result')))
            elif status == 'failed':
                result = 'failed'
            else:
                continue

            t = timestamp_pb2.Timestamp()
            t.FromSeconds(int(_REDIS_CONN.hget(k, 'ended_at')))
            jobs.append(server_pb2.JobDetails(id=k.partition(':')[2], result=result, ended_at=t))

        return server_pb2.JobList(jobs=jobs)

def _run_server():
    """Start a server in a subprocess."""
    _LOGGER.info('Starting new server.')
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=_PROCESS_COUNT))
    server_pb2_grpc.add_WorkerManagementServicer_to_server(WorkerManagement(), server)
    server_pb2_grpc.add_JobManagementServicer_to_server(JobManagement(), server)
    server.add_insecure_port(_BIND_ADDRESS)
    server.start()
    server.wait_for_termination()

def _init_redis_connection():
    global _REDIS_CONN

    _REDIS_CONN = Redis()

def main():
    _LOGGER.info("Binding to '%s'", _BIND_ADDRESS)
    sys.stdout.flush()
    _init_redis_connection()
    try:
        _run_server()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    main()
