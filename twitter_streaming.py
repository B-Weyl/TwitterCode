import tweepy
import secrets

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)


def analyze_status(text):
    if 'RT' in text[0:3]:
        print("This status was retweeted!")
        print(text)
    else:
        print("This status was not retweeted!")
        print(text)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.retweeted:
            print("This status was marked as retweeted")
            print(status.text)
        # analyze_status(status.text)
    def on_error(self, status_code):
        print(status_code)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=twitter_api.auth, listener=myStreamListener)
myStream.filter(track=['Trump'])


