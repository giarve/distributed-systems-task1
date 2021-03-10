# -*- coding: utf-8 -*-
from redis import Redis
from rq import Connection, Queue, Worker

import requests

_REDIS_QUEUE = None

# Count word frequencies of a text
def word_count_frequencies(url):
    resp = requests.get(url)

    wordfreq = {}
    for w in resp.text.split():
        if w in wordfreq:
            wordfreq[w] += 1
        else:
            wordfreq[w] = 1

    return wordfreq

# Count the total number of words
def count_words_from_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

def sum_partial_jobs_count_words(job_list):
    aggregate = 0

    for job_id in job_list:
        job = _REDIS_QUEUE.fetch_job(job_id)
        aggregate += job.result

    print("sum_partial_jobs_count_words aggregate: {}".format(aggregate))

    return aggregate

def sum_partial_jobs_word_count_frequencies(job_list):
    aggregate = {}
    
    for job_id in job_list:
        job = _REDIS_QUEUE.fetch_job(job_id)
        for k, v in job.result.items():
            val = aggregate.get(k, 0)
            val += v
            aggregate[k] = val

    print("sum_partial_jobs_word_count_frequencies aggregate: {}".format(aggregate))

    return aggregate
        
def worker_init():
    global _REDIS_QUEUE

    with Connection():
        _REDIS_QUEUE = Queue()
        Worker(_REDIS_QUEUE).work()
