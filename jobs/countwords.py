def count_words(url):
    import requests

    resp = requests.get(url)
    return len(resp.text.split())

def count_words_reduce(results):
    aggregate = 0

    for result in results:
        aggregate += result

    print("sum_partial_jobs_count_words aggregate: {}".format(aggregate))

    return aggregate