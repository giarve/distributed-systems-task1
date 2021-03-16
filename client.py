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

import webui

import pickle

import jobs

_server_channel_singleton = None
_server_workmgmt_stub_singleton = None
_server_jobmgmt_stub_singleton = None


def _initialize_server_conn(server_address):
    global _server_channel_singleton  # pylint: disable=global-statement
    global _server_workmgmt_stub_singleton  # pylint: disable=global-statement
    global _server_jobmgmt_stub_singleton  # pylint: disable=global-statement
    _server_channel_singleton = grpc.insecure_channel(server_address)
    _server_workmgmt_stub_singleton = server_pb2_grpc.WorkerManagementStub(
        _server_channel_singleton)
    _server_jobmgmt_stub_singleton = server_pb2_grpc.JobManagementStub(
        _server_channel_singleton)
    atexit.register(_shutdown_worker)

@click.group()
def worker():
    pass

def create_rpc(num):
    return _server_workmgmt_stub_singleton.create(server_pb2.NumberOfWorkers(num=num)).ok

@worker.command()
@click.argument('num', type=int, default=1)
def create(num):
    return create_rpc(num)

@worker.command()
def list():
    return list_rpc()

def list_rpc():
    return _server_workmgmt_stub_singleton.list(empty_pb2.Empty()).id

def delete_rpc(workerid):
    print(_server_workmgmt_stub_singleton)
    print(workerid)
    return _server_workmgmt_stub_singleton.delete(server_pb2.WorkerId(id=workerid)).ok

@worker.command()
@click.argument('workerid', type=int)
def delete(workerid):
    return delete_rpc(workerid)


@click.group()
def job():
    pass

@job.command()
@click.argument('jobname', required=True)
@click.argument('args', nargs=-1, required=True)
def run(jobname, args):
    map_func = getattr(jobs, jobname)
    reduce_func = getattr(jobs, jobname + "_reduce")
    map_function_pickled = pickle.dumps(map_func)
    reduce_function_pickled = pickle.dumps(reduce_func)
    return _server_jobmgmt_stub_singleton.create(server_pb2.WorkType(map_function_pickled=map_function_pickled, reduce_function_pickled=reduce_function_pickled, args=args))

@job.command()
def list():
    return _server_jobmgmt_stub_singleton.list(empty_pb2.Empty()).jobs

@click.group()
def cli():
    pass

@click.command()
@click.pass_context
def serve(ctx):
    webui.webui_serve(ctx)

class ServerConnection:
    _server_channel_singleton = None
    _server_workmgmt_stub_singleton = None
    _server_jobmgmt_stub_singleton = None

    def _shutdown_worker(self):
        if _server_channel_singleton is not None:
            _server_channel_singleton.close()

    def __init__(self):
        self._server_channel_singleton = grpc.insecure_channel(server_address)
        self._server_workmgmt_stub_singleton = server_pb2_grpc.WorkerManagementStub(
            _server_channel_singleton)
        self._server_jobmgmt_stub_singleton = server_pb2_grpc.JobManagementStub(
            _server_channel_singleton)
        atexit.register(self._shutdown_worker)

if __name__ == '__main__':
    #_initialize_server_conn("localhost:12312")
    connection = ServerConnection()

    cli.add_command(worker)
    cli.add_command(job)
    cli.add_command(serve)
    print(_server_workmgmt_stub_singleton)
    server_retval = cli(standalone_mode=False)
    print("Server says: {}".format(str(server_retval)))