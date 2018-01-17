import tweepy
import secrets
import os
import string
import re
import fnmatch


auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)

# get the status from the stream, and get the user bio
# if the user bio has a social media account, grab that
# write that account to a file


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.user.description:
            # print(status.user.description)
            # f.write(no_emoji(status.user.description) + '\n')
            find_social_accounts(no_emoji(status.user.description))

    def on_error(self, status_code):
        print(status_code)


def no_emoji(tweet):
    tweet = list(filter(lambda x: x in string.printable, tweet))
    new_string = ''.join(tweet)
    return new_string.strip()


def get_filter():
    topic = str(input("Topic to stream data from: "))
    return topic


def find_social_accounts(bio):
    with open('accounts.txt', 'a') as account_file:
        words = bio.split(' ')
        for word in words:
            if fnmatch.fnmatch(str(word), 'ig?'):
                print("Wrote an Instagram username to the file")
                the_index = int(words.index(word))
                if the_index + 1 < len(words):
                    # need a better way to handle cases with values found at the end of bio
                    if len(words[the_index + 1]) > 0:
                        account_file.write(
                            'Instagram account - ' + words[the_index + 1] + '\n')
            if fnmatch.fnmatch(str(word), 'insta?'):
                print("Wrote an Instagram username to the file")
                the_index = int(words.index(word))
                if the_index + 1 < len(words):
                    # need a better way to handle cases with values found at the end of bio
                    if len(words[the_index + 1]) > 0:
                        account_file.write(
                            'Instagram account - ' + words[the_index + 1] + '\n')
            if fnmatch.fnmatch(str(word), 'sc?'):
                print("Wrote a snapchat username to the file")
                the_index = int(words.index(word))
                if the_index + 1 < len(words):
                    # need a better way to handle cases with values found at the end of bio
                    if len(words[the_index + 1]) > 0:
                        account_file.write(
                            'Snapchat account  -  ' + words[the_index + 1] + '\n')
            if fnmatch.fnmatch(str(word), 'snap?'):
                print("Wrote a snapchat username to the file")
                the_index = int(words.index(word))
                if the_index + 1 < len(words):
                    # need a better way to handle cases with values found at the end of bio
                    if len(words[the_index + 1]) > 0:
                        account_file.write(
                            'Snapchat account  -  ' + words[the_index + 1] + '\n')
            else:
                continue


def main():
    if os.path.isfile('accounts.txt'):
        os.remove('accounts.txt')
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=twitter_api.auth, listener=myStreamListener)
    myStream.filter(track=[get_filter()])
    filter_bios()


if __name__ == '__main__':
    main()
