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

import dill as pickle

import jobs

_conn = None

@click.group()
def worker():
    pass

@worker.command()
@click.argument('num', type=int, default=1)
def create(num):
    return _conn.server_workmgmt_stub_singleton.create(server_pb2.NumberOfWorkers(num=num)).ok

@worker.command()
def list():
    return _conn.server_workmgmt_stub_singleton.list(empty_pb2.Empty()).workers

@worker.command()
@click.argument('workerid', type=int)
def delete(workerid):
    return _conn.server_workmgmt_stub_singleton.delete(server_pb2.WorkerId(id=workerid)).ok


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
    return _conn.server_jobmgmt_stub_singleton.create(server_pb2.WorkType(map_function_pickled=map_function_pickled, reduce_function_pickled=reduce_function_pickled, args=args))

@job.command()
def list():
    return _conn.server_jobmgmt_stub_singleton.list(empty_pb2.Empty()).jobs

@click.group()
def cli():
    pass

@click.command()
def serve():
    webui.webui_serve(_conn)

class ServerConnection:
    _server_channel_singleton = None
    server_workmgmt_stub_singleton = None
    server_jobmgmt_stub_singleton = None

    def _shutdown_worker(self):
        if self._server_channel_singleton is not None:
            self._server_channel_singleton.close()

    def __init__(self, server_address):
        self._server_channel_singleton = grpc.insecure_channel(server_address)
        self.server_workmgmt_stub_singleton = server_pb2_grpc.WorkerManagementStub(
            self._server_channel_singleton)
        self.server_jobmgmt_stub_singleton = server_pb2_grpc.JobManagementStub(
            self._server_channel_singleton)
        atexit.register(self._shutdown_worker)

    

if __name__ == '__main__':
    _conn = ServerConnection("localhost:12312")

    cli.add_command(worker)
    cli.add_command(job)
    cli.add_command(serve)
    server_retval = cli(standalone_mode=False)
    print("Server says: {}".format(str(server_retval)))