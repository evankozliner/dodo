from os import environ
from twitter import Twitter, OAuth

def tweet(twt):
    twitter = user_level_auth()
    twitter.statuses.update(status=twt)

def user_level_auth():
    """ Uses environment variables for user level auth on twitter """
    CONSUMER_KEY = environ.get('BOT_CONSUMER_KEY')
    CONSUMER_SECRET = environ.get('BOT_CONSUMER_SECRET')
    ACCESS_TOKEN = environ.get('BOT_ACCESS_TOKEN')
    ACCESS_SECRET = environ.get('BOT_ACCESS_SECRET')
    return Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

