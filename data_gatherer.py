from twitter import Twitter, OAuth2, TwitterHTTPError, oauth2_dance
from os import environ
from datetime import datetime, timedelta
from dateutil import parser
from time import time
import csv
import json

def main():
    """ By Evan Kozliner & Wilfred Denton
    Gathers tweets to train a machine learning model on by fetching tweets before the 
    current time."""
    start_time = time()
    tweet_ids = set([])
    tweets_csv = open("tweets.csv", "w")
    writer = csv.writer(tweets_csv, lineterminator="\n")
    metadata_file = open("metadata.csv", "w+")
    config = json.load(open("config.json"))
    WOEID = int(config["WOEID"])
    total_tweets_fetched = 0
    cutoff_day_reached = False
    timeline_specifier = ""
    num_tweets = int(config["tweets_per_request"]) 
    num_requests = 0
    # Using 1 day ago as the cutoff time
    cutoff_conf = config["cutoff"]
    time_diff = timedelta(hours=int(cutoff_conf["hours"]), 
            minutes=int(cutoff_conf["minutes"]),
            days=int(cutoff_conf["days"]),
            weeks=int(cutoff_conf["weeks"]))
    cutoff_date = datetime.utcnow() - time_diff
    bool(config["exclude_retweets"])
    rt_str = ("exclude:retweets " if config["exclude_retweets"] == 'true' else "")

    twitter = application_level_auth()
    search_term = (config["search_term"].encode('utf-8') if bool(config['search_term']) \
            else get_top_trend(twitter, WOEID))

    #writer.writerow("body") # body line to match example
    while not cutoff_day_reached:
        tweets = query_twitter(timeline_specifier + rt_str + search_term,
                twitter, num_tweets)
        num_requests += 1
        total_tweets_fetched += len(tweets) 
        for tweet in tweets:
            tweet_ids.add(tweet['id'])
            #writer.writerow(tweet['text'].encode('utf-8').replace('\n', '\t') + "\n")
            #writer.writerow([tweet['text'].encode('utf-8').replace('\n', '\t')])
            #writer.writerow([tweet['text'].encode('utf-8')])
            tweets_csv.write(tweet['text'].encode('utf-8').replace('\n', '\t') + "\n")

            #if "\n" in tweet['text']:
            #    tweets_csv.write("'" + tweet['text'].encode('utf-8')
        timeline_specifier = "max_id:" + str(min(tweet_ids)) + " " 
        cutoff_day_reached = was_cutoff_reached(tweets, cutoff_date)

    metadata_file.write("hashtag_searched," + search_term + "\n")
    metadata_file.write("tweets_fetched," + str(total_tweets_fetched) + "\n")
    metadata_file.write("woeid," + str(WOEID) + "\n")
    metadata_file.write("max_tweet," + str(max(tweet_ids)) + "\n")
    metadata_file.write("min_tweet," + str(min(tweet_ids)) + "\n")
    metadata_file.write("time_minutes," + str((time() - start_time)/60) + "\n")
    metadata_file.write("requests," + str(num_requests) + "\n")
    test_duplicates(tweet_ids, total_tweets_fetched)
    tweets_csv.close()
    metadata_file.close()

def was_cutoff_reached(tweets, cutoff_date):
    """ Tests if one of the tweets time is before the cutoff date"""
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

def application_level_auth():
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
