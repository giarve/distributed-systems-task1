#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Task 1: High Performance Computing Cluster"""

import atexit
import logging
import sys

from google.protobuf import empty_pb2
import grpc

import click

import server_pb2
import server_pb2_grpc

_server_channel_singleton = None
_server_stub_singleton = None

def _shutdown_worker():
    if _server_channel_singleton is not None:
        _server_channel_singleton.close()


def _initialize_server_conn(server_address):
    global _server_channel_singleton  # pylint: disable=global-statement
    global _server_stub_singleton  # pylint: disable=global-statement
    _server_channel_singleton = grpc.insecure_channel(server_address)
    _server_stub_singleton = server_pb2_grpc.WorkerManagementStub(
        _server_channel_singleton)
    atexit.register(_shutdown_worker)

@click.group()
def worker():
    pass

@worker.command()
def create():
    return _server_stub_singleton.create(empty_pb2.Empty()).ok

@worker.command()
def list():
    return _server_stub_singleton.list(empty_pb2.Empty()).id

@worker.command()
@click.argument('workerid', type=int)
def delete(workerid):
    return _server_stub_singleton.delete(server_pb2.WorkerId(id=workerid)).ok

@click.group()
def job():
    pass

@job.command()
@click.argument('urls', nargs=-1, required=True)
def run_wordcount(urls):
    return _server_stub_singleton.job(server_pb2.WorkType(program=server_pb2.WorkType.Program.WORDCOUNT, urls=urls))

@job.command()
@click.argument('urls', nargs=-1, required=True)
def run_countwords(urls):
    return _server_stub_singleton.job(server_pb2.WorkType(program=server_pb2.WorkType.Program.COUNTWORDS, urls=urls))


@click.group()
def cli():
    pass

if __name__ == '__main__':
    _initialize_server_conn("localhost:12312")
    cli.add_command(worker)
    cli.add_command(job)
    server_retval = cli(standalone_mode=False)
    print("Server says: {}".format(str(server_retval)))