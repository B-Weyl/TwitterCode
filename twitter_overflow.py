import tweepy
import secrets

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)

tweets = twitter_api.user_timeline()
username = ''
limit = 10
for status in tweepy.Cursor(twitter_api.user_timeline, screen_name=username).items(limit):
    print(str(status.place))
