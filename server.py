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

_LOGGER = logging.getLogger(__name__)

_PROCESS_COUNT = multiprocessing.cpu_count()

_WORKER_ID = 0
_WORKERS = {}

_BIND_ADDRESS = 'localhost:12312'

class WorkerManagement(server_pb2_grpc.WorkerManagementServicer):

    def create(self, request, context):  
        global _WORKER_ID
        
        worker = multiprocessing.Process(target=wk.worker_init)
        worker.start()
        _WORKERS[_WORKER_ID] = worker
        _LOGGER.info('Creating a worker %s', worker)
        _WORKER_ID += 1

        return server_pb2.Status(ok=True)

    def listWorkers(self, request, context):
        return server_pb2.WorkerList(id=_WORKERS.keys())

    def delete(self, request, context):
        worker = _WORKERS.pop(request.id, None)
        if worker is None:
            return server_pb2.Status(ok=False)

        _LOGGER.info('Terminating the worker %s', request.id)
        worker.terminate()
        return server_pb2.Status(ok=True)

    def job(self, request, context):
        print(request)
        return server_pb2.JobId(id=1)

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


def main():
    # _BIND_ADDRESS = 'localhost:{}'.format(port)
    _LOGGER.info("Binding to '%s'", _BIND_ADDRESS)
    sys.stdout.flush()
    _run_server()


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    main()
