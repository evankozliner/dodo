from twitter import Twitter, OAuth2, TwitterHTTPError, oauth2_dance
from os import environ
from datetime import datetime, timedelta
from dateutil import parser

def main():
    """ By Evan Kozliner & Wilfred Denton
    Gathers tweets to train a machine learning model on. """
    tweet_ids = set([])
    tweets_csv = open("tweets.csv", "w+")
    metadata_file = open("metadata.csv", "w+")
    WOEID = 2383660 # Yahoo Where On Earth ID for Columbus 
    total_tweets_fetched = 0
    min_tweet_id = 0
    cutoff_day_reached = False
    timeline_specifier = ""
    NUMBER_OF_TWEETS_TO_FETCH = 100
    # Using 1 day ago as the cutoff time
    cutoff_date = datetime.utcnow() - timedelta(hours=3)

    twitter = get_twitter_env()
    top_trend_hashtag = get_top_trend(twitter, WOEID)

    while not cutoff_day_reached:
        tweets = query_twitter(timeline_specifier + "exclude:retweets " + top_trend_hashtag,
                twitter, NUMBER_OF_TWEETS_TO_FETCH)
        total_tweets_fetched += len(tweets) 
        for tweet in tweets:
            tweet_ids.add(tweet['id'])
            tweets_csv.write(str(tweet['text'].encode('utf-8')) + "\n")
        timeline_specifier = "max_id:" + str(min(tweet_ids)) + " " 
        cutoff_day_reached = was_cutoff_reached(tweets, cutoff_date)

    metadata_file.write("hashtag_searched," + top_trend_hashtag + "\n")
    metadata_file.write("tweets_fetched," + str(total_tweets_fetched) + "\n")
    metadata_file.write("woeid," + str(WOEID) + "\n")
    metadata_file.write("max_tweet," + str(max(tweet_ids)) + "\n")
    metadata_file.write("min_tweet," + str(min(tweet_ids)) + "\n")
    test_duplicates(tweet_ids, total_tweets_fetched)
    tweets_csv.close()
    metadata_file.close()

def was_cutoff_reached(tweets, cutoff_date):
    for tweet in tweets:
        date = parser.parse(tweet['created_at'].encode('utf-8')).replace(tzinfo=None)
        #print date.strftime("%H:%M:%S")
        if cutoff_date > date:
            return True
    return False

def query_twitter(query, twitter, num_tweets):
    """ Does a /search/tweets query on twitter only returning statuses. """
    return twitter.search.tweets(q=query, 
            result_type='recent', 
            lang='en', 
            count=num_tweets)['statuses']

def get_top_trend(twitter, WOEID):
    """ Returns the top trends for a specific WOEID (Yahoo Where On Eath Id). """
    trends = twitter.trends.place(_id = WOEID)
    return trends[0]['trends'][0]['name'].encode('utf-8')

def get_twitter_env():
    """ Uses environment variables to get an application-level authentication from twitter. """
    CONSUMER_KEY = environ.get('BOT_CONSUMER_KEY')
    CONSUMER_SECRET = environ.get('BOT_CONSUMER_SECRET')
    BEARER_TOKEN = oauth2_dance(CONSUMER_KEY, CONSUMER_SECRET)
    return Twitter(auth=OAuth2(bearer_token=BEARER_TOKEN))

def test_duplicates(tweet_ids, total_tweets):
    if len(tweet_ids) == total_tweets:
        print "No duplicates."
if __name__ == "__main__":
    main()
