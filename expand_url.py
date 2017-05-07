import tweepy
import secrets
from urllib import parse as urlparse
auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)

username = 'Bweyl_'
limit = 100

urls = []
for status in tweepy.Cursor(twitter_api.user_timeline, screenname=username).items(limit):
    if status.entities['urls']:
        for url in status.entities['urls']:
            links = url['expanded_url']
            print(status.text + links)



