import nltk.data
import re

def pull_tweet():
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    samples = open('sample.txt').read()
    tweet = samples[-2000:].split('\n---------\n')[3]
    tweet = re.sub(r'-+', ' ', tweet)[:140]
    return tweet
