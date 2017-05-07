import tweepy
import secrets

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)

all_trends = twitter_api.trends_available()
for trend in all_trends:
    if trend['name'] == 'Philadelphia':
        print(trend)