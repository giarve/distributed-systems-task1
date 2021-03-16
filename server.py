#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Task 1: High Performance Computing Cluster"""

from concurrent import futures
import contextlib
import datetime
import logging
import math
import multiprocessing
import time
import sys

import grpc

import server_pb2
import server_pb2_grpc
from google.protobuf import timestamp_pb2

import worker as wk

from redis import Redis
from rq import Queue

_LOGGER = logging.getLogger(__name__)

_PROCESS_COUNT = multiprocessing.cpu_count()

_WORKER_ID = 0
_WORKERS = {}

_BIND_ADDRESS = 'localhost:12312'

_REDIS_QUEUE = None

class WorkerManagement(server_pb2_grpc.WorkerManagementServicer):

    def create(self, request, context):  
        global _WORKER_ID
        
        _LOGGER.info('Creating %d workers', request.num)

        for _ in range(request.num):
            worker = multiprocessing.Process(target=wk.worker_init)
            worker.start()
            _WORKERS[_WORKER_ID] = worker
            _LOGGER.info('Creating a worker %s', worker)
            _WORKER_ID += 1

        return server_pb2.Status(ok=True)

    def list(self, request, context):
        return server_pb2.WorkerList(id=_WORKERS.keys())

    def delete(self, request, context):
        worker = _WORKERS.pop(request.id, None)
        if worker is None:
            return server_pb2.Status(ok=False)

        _LOGGER.info('Terminating the worker %s', request.id)
        worker.terminate()
        return server_pb2.Status(ok=True)
        

class JobManagement(server_pb2_grpc.JobManagementServicer):
    def create(self, request, context):
        arg_list = list(request.args)
        job_list = []

        if len(arg_list) > 1:
            for arg in arg_list:
                job_list.append(_REDIS_QUEUE.enqueue(wk.worker_execute, request.map_function_pickled, arg))

            job_id_list = list(map(lambda x: x.id, job_list))
            reduce_job = _REDIS_QUEUE.enqueue(wk.worker_execute_reduce, request.reduce_function_pickled, job_id_list, depends_on=job_list)
            return server_pb2.JobId(id=reduce_job.id)
        else:
            arg = arg_list[0] if len(arg_list) > 0 else None
            job = _REDIS_QUEUE.enqueue(wk.worker_execute, request.map_function_pickled, arg)
            return server_pb2.JobId(id=job.id)
    
    def list(self, request, context):
        jobs = []
        for job_id in _REDIS_QUEUE.finished_job_registry.get_job_ids():
            job = _REDIS_QUEUE.fetch_job(job_id)
            t = timestamp_pb2.Timestamp()
            t.FromDatetime(job.ended_at)
            jobs.append(server_pb2.JobDetails(id=job_id, result=str(job.result), ended_at=t))

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
    global _REDIS_QUEUE

    _REDIS_QUEUE = Queue(connection=Redis())

def main():
    _LOGGER.info("Binding to '%s'", _BIND_ADDRESS)
    sys.stdout.flush()
    _init_redis_connection()
    _run_server()


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    main()
