import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
samples = open('sample.txt').read()
print samples[-1000:].split('\n')[1]
