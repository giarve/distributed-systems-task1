"""Task 1: High Performance Computing Cluster"""

import atexit
import logging
import sys

import grpc

import click

import server_pb2
import server_pb2_grpc

_server_channel_singleton = None
_server_stub_singleton = None

_LOGGER = logging.getLogger(__name__)


def _shutdown_worker():
    _LOGGER.info('Shutting worker process down.')
    if _server_channel_singleton is not None:
        pass
        #_server_channel_singleton.stop()


def _initialize_server_conn(server_address):
    global _server_channel_singleton  # pylint: disable=global-statement
    global _server_stub_singleton  # pylint: disable=global-statement
    _LOGGER.info('Initializing worker process.')
    _server_channel_singleton = grpc.insecure_channel(server_address)
    _server_stub_singleton = server_pb2_grpc.WorkerManagementStub(
        _server_channel_singleton)
    atexit.register(_shutdown_worker)

@click.group()
def worker():
    pass

@worker.command()
def create():
    return _server_stub_singleton.create(server_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty())

@worker.command()
def list():
    return _server_stub_singleton.listWorkers(server_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty())

@worker.command()
def delete(workerId):
    return _server_stub_singleton.delete(server_pb2.WorkerId(id=workerId))

@click.group()
def job():
    pass

@job.command()
def run_wordcount(urls):
    return _server_stub_singleton.job(server_pb2.WorkType(programName="wordcount", urls=urls))

@job.command()
def run_countwords(urls):
    return _server_stub_singleton.job(server_pb2.WorkType(programName="countwords", urls=urls))


@click.group()
def cli():
    pass

def main():
    _initialize_server_conn("localhost:12312")
    #print(create_worker())
    cli.add_command(worker)
    cli.add_command(job)
    cli()
    # print(add_job_to_queue(programName="wordcount", urls=["url1", "url2"]))


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    _LOGGER.setLevel(logging.INFO)
    main()
