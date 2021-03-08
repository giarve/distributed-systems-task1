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

_ONE_DAY = datetime.timedelta(days=1)
_PROCESS_COUNT = multiprocessing.cpu_count()

_WORKERS = []

_BIND_ADDRESS = 'localhost:12312'

class WorkerManagement(server_pb2_grpc.WorkerManagementServicer):

    def create(self, request, context):  
        worker = multiprocessing.Process(target=wk.worker_init)
        worker.start()
        _WORKERS.append(worker)
        _LOGGER.info('Creating a worker %s', worker)

        return server_pb2.Status(ok=True)

    def listWorkers(self, request, context):
        return server_pb2.WorkerList(id=[])
        # return _WORKERS

    def delete(self, request, context):
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
