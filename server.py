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

import worker as wk

from redis import Redis
from rq import Queue

_LOGGER = logging.getLogger(__name__)

_PROCESS_COUNT = multiprocessing.cpu_count()

_WORKER_ID = 0
_WORKERS = {}

_BIND_ADDRESS = 'localhost:12312'

_REDIS_QUEUE = None

# Convert the proto type to the real function name      
_PROGRAM_TO_WORK_FUNC = {
    server_pb2.WorkType.Program.COUNTWORDS: wk.count_words_from_url,
    server_pb2.WorkType.Program.WORDCOUNT: wk.word_count_frequencies
}

_PROGRAM_TO_AGGREGATE_FUNC = {
    server_pb2.WorkType.Program.COUNTWORDS: wk.sum_partial_jobs_count_words,
    server_pb2.WorkType.Program.WORDCOUNT: wk.sum_partial_jobs_word_count_frequencies
}

class WorkerManagement(server_pb2_grpc.WorkerManagementServicer):

    def create(self, request, context):  
        global _WORKER_ID
        
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

    def job(self, request, context):
        job_function = _PROGRAM_TO_WORK_FUNC.get(request.program, None)
        job_aggregate_function = _PROGRAM_TO_AGGREGATE_FUNC.get(request.program, None)

        url_list = list(request.urls)
        url_list_len = len(url_list)

        if job_function is None:
            return server_pb2.JobId(id="INVALID job CASE")
        
        if url_list_len == 0:
            return server_pb2.JobId(id="No URLs provided")

        job_list = []

        if url_list_len > 1:
            for url in url_list:
                job_list.append(_REDIS_QUEUE.enqueue(job_function, url))

            job_id_list = list(map(lambda x: x.id, job_list))
            print(job_id_list)
            reduce_job = _REDIS_QUEUE.enqueue(job_aggregate_function, job_id_list, depends_on=job_list)
            return server_pb2.JobId(id=reduce_job.id)
        else:
            job = _REDIS_QUEUE.enqueue(job_function, url_list[0])
            return server_pb2.JobId(id=job.id)

def _run_server():
    """Start a server in a subprocess."""
    _LOGGER.info('Starting new server.')
    options = (('grpc.so_reuseport', 1),)

    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=_PROCESS_COUNT), options=options)
    server_pb2_grpc.add_WorkerManagementServicer_to_server(WorkerManagement(), server)
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
