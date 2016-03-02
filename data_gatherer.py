import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from os import environ

known_tweets = []
id_file = open("existing_tweets.txt", 'w+')
known_tweets = map(lambda x: int(x), id_file.read().splitlines())

ACCESS_TOKEN = environ.get('BOT_ACCESS_TOKEN')
ACCESS_SECRET = environ.get('BOT_ACCESS_SECRET')
CONSUMER_KEY = environ.get('BOT_CONSUMER_KEY')
CONSUMER_SECRET = environ.get('BOT_CONSUMER_SECRET')
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)

columbus_trends = twitter.trends.place(_id = 2383660) #get columbus trends

top_trend_hashtag = columbus_trends[0]['trends'][0]['name']
ids = []
tweets = twitter.search.tweets(q=top_trend_hashtag, result_type='recent', lang='en', count=100)
# filter retweets and already gathered tweets
tweets = filter(lambda x: (not x['id'] in known_tweets) and (not x['retweeted']), 
        tweets['statuses'])

for tweet in tweets:
    id_file.writeln(str(tweet['id']))
    print tweet['text']
