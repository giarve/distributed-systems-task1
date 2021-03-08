# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from rq import Connection, Queue, Worker

def worker_init():
    # Tell rq what Redis connection to use
    with Connection():
        q = Queue()
        Worker(q).work()