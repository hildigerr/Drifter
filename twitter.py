import configparser
import tweepy

def getAPI():
    config = configparser.ConfigParser()
    config.read('twitter.conf')

    if 'twitter' in config:
        if config.has_option('twitter', 'consumer_key'):
            consumer_key = config['twitter']['consumer_key']
        else:
            return None
        if config.has_option('twitter', 'consumer_secret'):
            consumer_secret = config['twitter']['consumer_secret']
        else:
            return None
        if config.has_option('twitter', 'access_token'):
            access_token = config['twitter']['access_token']
        else:
            return None
        if config.has_option('twitter', 'access_token_secret'):
            access_token_secret = config['twitter']['access_token_secret']
        else:
            return None
    else:
        return None

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def sendTweet(msg):
    return True

