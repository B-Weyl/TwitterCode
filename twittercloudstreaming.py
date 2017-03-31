import tweepy
from wordcloud import WordCloud, STOPWORDS
import secrets
import argparse
import numpy
import collections
import datetime
import re
from os import path
import os
import matplotlib.pyplot as plt
from cloud import cloud


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

parser = argparse.ArgumentParser(description= "WordClouds of users tweets",
                                 usage='%(prog)s -f <@tweet_filter> [options]')
parser.add_argument('-l', '--limit', metavar='N', type=int, default=1000,
                    help='limit the number of tweets to get that contain that filter')
parser.add_argument('-s', '--scope', required=True, metavar="tweet_scope",
                    help='target tweet_scope')
parser.add_argument('-g', '--geolocation', metavar="geolocation",
                    help='target geolocation')
parser.add_argument('-e', '--eggs', default=False, metavar="eggs",
                    help='target eggs')
args = parser.parse_args()

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)


def file_check(filename):
    filename = args.scope + '.txt'
    if os.path.isfile(filename):
        os.remove(filename)


def write_status(text):
    with open(args.scope + '.txt', 'ab') as writefile:
        writefile.write(text.encode('UTF-8') + b'\n')


class MyStreamListener(tweepy.StreamListener):
    file_check(args.scope + '.txt')

    def on_status(self, status):
        if args.eggs:
            if args.geolocation:
                if status.author.location == args.geolocation:
                    write_status(status.text.lower())
            if not status.author.default_profile_image:
                write_status(status.text.lower())
        else:
            write_status(status.text.lower())

    def on_error(self, status_code):
        print(status_code)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=twitter_api.auth, listener=myStreamListener)
myStream.filter(track=[args.scope])
cloud(args.scope + '.txt')


