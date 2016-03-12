import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from os import environ

"""
    
"""
known_tweets = []
ids = []
id_file = open("existing_tweets.txt", 'w+')
tweets_csv = open("tweets.csv", "w+")
metadata_file = open("metadata.csv", "w+")
known_tweets = map(lambda x: int(x), id_file.read().splitlines())
WOEID = 2383660 # Yahoo Where On Earth ID for Columbus 
NUMBER_OF_TWEETS_TO_FETCH = 15
metadata_file.write("tweets_fetched," + str(NUMBER_OF_TWEETS_TO_FETCH) + "\n")
metadata_file.write("woeid," + str(WOEID) + "\n")

ACCESS_TOKEN = environ.get('BOT_ACCESS_TOKEN')
ACCESS_SECRET = environ.get('BOT_ACCESS_SECRET')
CONSUMER_KEY = environ.get('BOT_CONSUMER_KEY')
CONSUMER_SECRET = environ.get('BOT_CONSUMER_SECRET')
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth=oauth)

columbus_trends = twitter.trends.place(_id = WOEID)

top_trend_hashtag = columbus_trends[0]['trends'][0]['name']
metadata_file.write("hashtag_searched," + top_trend_hashtag + "\n")
# Exclude any retweets
top_trend_hashtag = "exclude:retweets " + top_trend_hashtag

tweets = twitter.search.tweets(q=top_trend_hashtag, 
        result_type='recent', 
        lang='en', 
        count=NUMBER_OF_TWEETS_TO_FETCH)['statuses']

percentage_of_retweets = float(len(filter(lambda x: 'retweeted_status' in x, tweets))) \
        / float(len(tweets))
metadata_file.write('percentage_of_retweets,' + str(percentage_of_retweets) + "\n")

# filter retweets and already gathered tweets
tweets = filter(lambda x: (not x['id'] in known_tweets) and (not 'retweeted_status' in x), 
        tweets)

for tweet in tweets:
    id_file.write(str(tweet['id']) + "\n")
    tweets_csv.write(str(tweet['text'].encode('utf-8')))
    
id_file.close()
tweets_csv.close()
metadata_file.close()
