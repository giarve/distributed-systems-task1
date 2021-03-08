
# Count the total number of words
def countingWords(text):
    return len(text.split())


# Count word frequencies of a text
def wordCount(text):
    wordlist = wordstring.split()
    wordfreq = []
    for w in wordlist:
        wordfreq.append(wordlist.count(w))
    return wordfreq