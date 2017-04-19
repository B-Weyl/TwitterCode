import tweepy
import secrets
import argparse


auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--woeid", help="the woeid of where trends should come from")
parser.add_argument("-t", "--top", default=10, type=int, help="the number of trends to get: default is 10")
parser.add_argument("-l", "--location", default='Philadelphia', type=str, help="the location of trends you would like to get")
parser.add_argument("-i", "--international", required=False, help="include international trends (non-usa)")
# parser.add_argument("-r", "--range", required=False, help="determines in how many places a trend is trending")
args = parser.parse_args()

# print(args.woeid)
# print(args.top)


def get_woeid_usa():
    places = twitter_api.trends_available()
    all_woeids = {place['name'].lower(): place['woeid'] for place in places}
    usa_woeids = {place['name'].lower(): place['woeid'] for place in places if place['country'] == 'United States'}
    if args.international:
        return all_woeids
    else:
        return usa_woeids


# def get_trend_range(trend):
#     """
#     given a trend, return all of the woeids with that trend
#     :param woeid:
#     :return:
#     """
#     places = twitter_api.trends_available()
#     all_woeids = {place['name']: place['woeid'] for place in places}
#     trending_places = []
#     for value in all_woeids.values():
#         if trend in twitter_api.trends_place(value):
#             trending_places.append(value)
#     return trending_places


def trends_and_volumes(woeid):
    """
    create a dict of trends from a certain woeid, and tweet_volume
    :return: dict
    """
    if args.woeid:
        woeid = args.woeid
    else:
        woeid = location_to_woeid(args.location)
    trending_topics = []
    tweet_volume = []
    woeid_trends = twitter_api.trends_place(woeid)
    for woeid_trend in woeid_trends:
        for x in range(args.top):
            trending_topics.append(woeid_trend['trends'][x]['name'])
            tweet_volume.append(woeid_trend['trends'][x]['tweet_volume'])
    trend_volume_dict = dict(zip(trending_topics, tweet_volume))
    return trend_volume_dict


def location_to_woeid(location):
    location = location.lower()
    trends = twitter_api.trends_available()
    error_string = "This location cannot be resolved to a WOEID"
    all_woeids = get_woeid_usa()
    if location in all_woeids:
        return all_woeids[location]
    else:
        # print('This is a list of all available locations to get trends from:')
        # names = []
        # for trend in trends:
        #     names.append(trend['name'])
        # print(names)
        raise ValueError('This location cannot be resolved to a WOEID')


def main():
    woeids = get_woeid_usa()
    print(trends_and_volumes(args.woeid))


if __name__ == '__main__':
    main()





