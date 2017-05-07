import tweepy
import secrets


auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)

print(twitter_api.search(q='snowflake', rpp=1))