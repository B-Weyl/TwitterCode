import tweepy
import secrets
import argparse
import matplotlib as plt


auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--woeid", required=True, help="the woeid of where trends should come from")
parser.add_argument("-t", "--top", default=10, type=int, help="the number of trends to get: default is 10")
parser.add_argument("-i", "--international", required=False, help="include international trends (non-usa)")
args = parser.parse_args()

print(args.woeid)
print(args.top)


def get_woeid_usa():
    trends = twitter_api.trends_available()
    all_woeids = {trend['name']: trend['woeid'] for trend in trends}
    usa_woeids = {trend['name']: trend['woeid'] for trend in trends if trend['country'] == 'United States'}
    if args.international:
        return all_woeids
    else:
        return usa_woeids


def trends_and_volumes(woeid):
    """
    create a dict of trends from a certain woeid, and tweet_volume
    :return: dict
    """
    woeid = args.woeid
    trending_topics = []
    tweet_volume = []
    if woeid.isnumeric():
        woeid_trends = twitter_api.trends_place(woeid)
        for woeid_trend in woeid_trends:
            for x in range(args.top):
                trending_topics.append(woeid_trend['trends'][x]['name'])
                tweet_volume.append(woeid_trend['trends'][x]['tweet_volume'])
    trend_volume_dict = dict(zip(trending_topics, tweet_volume))
    return trend_volume_dict


def location_to_woeid(location):
    trends = twitter_api.trends_available()
    error_string = "This location cannot be resolved to a WOEID"
    all_woeids = {trend['name']: trend['woeid'] for trend in trends}
    if location in all_woeids:
        return all_woeids[location]
    else:
        return error_string
    

def main():
    woeids = get_woeid_usa()
    print(trends_and_volumes(args.woeid))


if __name__ == '__main__':
    main()





