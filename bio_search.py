import tweepy
import secrets
import os
import string
import re

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        with open('bios.txt', 'a') as f:
            if status.user.description:
                # print(status.user.description)
                # f.write(no_emoji(status.user.description) + '\n')
                f.write(no_emoji(filter_bios(status.user.description)))

    def on_error(self, status_code):
        print(status_code)


def no_emoji(tweet):
    tweet = list(filter(lambda x: x in string.printable, tweet))
    new_string = ''.join(tweet)
    new_string = new_string.replace('QR Code Link to This Post', '')
    return new_string.strip()


def filter_bios(bio):
    profiles = []
    for word in bio:
        if 'IG' or 'ig' in word:
            profiles.append(word)
    return profiles


def contains_profiles(word):
    if word:
        if 'IG' in word:
            return word


def main():
    if os.path.isfile('bios.txt'):
        os.remove('bios.txt')
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=twitter_api.auth, listener=myStreamListener)
    myStream.filter(track=['Sex'])
    filter_bios()


if __name__ == '__main__':
    main()
