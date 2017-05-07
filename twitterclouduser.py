#! /usr/local/bin/python3

import tweepy
from wordcloud import WordCloud, STOPWORDS
import secrets
import argparse
import numpy
import collections
import datetime
import re
import os
from os import path
import matplotlib.pyplot as plt

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

parser = argparse.ArgumentParser(description="WordClouds of users tweets",
                                 usage='%(prog)s -n <@screen_name> [options]')
parser.add_argument('-l', '--limit', metavar='N', type=int, default=1000,
                    help='limit the number of tweets to get')
parser.add_argument('-n', '--name', required=True, metavar="screen_name",
                    help='target screen_name')

args = parser.parse_args()

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)


def get_tweets(api, username, limit):
    filename = args.name + '_tweets.txt'
    # if the file is already present, we want to remove it and get the most 
    # recent tweets
    if os.path.isfile(filename):
        os.remove(filename)
    for status in tweepy.Cursor(api.user_timeline, screen_name=username).items(
            limit):
        # print(status)
        write_tweets(status.text)


def get_tweet_time(tweet):
    filename = args.name + '_tweet_dates.txt'
    with open(filename, 'ab') as tweet_dates:
        tweet_dates.write(tweet.created_at + b'\n')


def write_tweets(tweet):
    filename = args.name + '_tweets.txt'
    with open(filename, 'ab') as tweet_content:
        tweet_content.write(clean_tweet(tweet).encode('UTF-8') + b'\n')


def clean_tweet(tweet):
    tweet = re.sub("https?\:\/\/", "", tweet)  # links
    tweet = re.sub("#\S+", "", tweet)  # hashtags
    tweet = re.sub("\.?@", "", tweet)  # at mentions
    tweet = re.sub("RT.+", "", tweet)  # Retweets
    tweet = re.sub("Video\:", "", tweet)  # Videos
    tweet = re.sub("\n", "", tweet)  # new lines
    tweet = re.sub("^\.\s.", "", tweet)  # leading whitespace
    tweet = re.sub("\s+", " ", tweet)  # extra whitespace
    tweet = re.sub("&amp;", "and", tweet)  # encoded ampersands
    return tweet


def cloud(username=args.name):
    # make the cloud
    d = path.dirname(__file__)
    text = open(path.join(d, username + '_tweets.txt'), encoding='UTF-8').read()
    # wordcloud = WordCloud().generate(text)
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def main():
    print("Hello")
    user_info = twitter_api.get_user(screen_name=args.name)
    num_tweets = numpy.amin([args.limit, user_info.statuses_count])
    print(user_info.statuses_count)
    print(args.limit)
    get_tweets(twitter_api, args.name, limit=num_tweets)
    cloud(username=args.name)
if __name__ == '__main__':
    main()
