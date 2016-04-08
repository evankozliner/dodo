import nltk
from nltk.tokenize import TweetTokenizer

tweets_file = open("data/tweets/input.txt")
tweets = tweets_file.read().replace('\n---------\n', '\n')
tknzr = TweetTokenizer(tweets)
tokens = tknzr.tokenize(tweets)
tweet_trigrams = nltk.trigrams(tokens)
text = nltk.Text(tweet_trigrams)
print text.generate(length=60)
