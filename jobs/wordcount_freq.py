# Count word frequencies of a text
def word_count_frequencies(url):
    import requests

    resp = requests.get(url)

    wordfreq = {}
    for w in resp.text.split():
        if w in wordfreq:
            wordfreq[w] += 1
        else:
            wordfreq[w] = 1

    return wordfreq

def word_count_frequencies_reduce(results):
    aggregate = {}
    
    for result in results:
        for k, v in result.items():
            val = aggregate.get(k, 0)
            val += v
            aggregate[k] = val

    print("sum_partial_jobs_word_count_frequencies aggregate: {}".format(aggregate))

    return aggregate
