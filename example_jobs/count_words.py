def map_func(url):
    import requests

    resp = requests.get(url)
    return len(resp.text.split())

def reduce_func(results):
    aggregate = 0

    for result in results:
        aggregate += result

    return aggregate

