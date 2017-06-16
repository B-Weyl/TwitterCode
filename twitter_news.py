import tweepy
import secrets
import argparse
import datetime
from ascii_graph import Pyasciigraph
import collections
from collections import OrderedDict
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
twitter_api = tweepy.API(auth)
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--woeid",
                    help="the woeid of where trends should come from")
parser.add_argument("-t", "--top", default=10, type=int,
                    help="the number of trends to get: default is 10")
# parser.add_argument("-l", "--location", default='Philadelphia', type=str,
#                     help="the location of trends you would like to get")
parser.add_argument('-lol', '--listoflocations', nargs='*',
                    help='a list of locations')
parser.add_argument("-q", "--query",
                    help="gives tweets for a certain topic")
args = parser.parse_args()


def get_woeid_usa():
    places = twitter_api.trends_available()
    all_woeids = {place['name'].lower(): place['woeid'] for place in places}
    return all_woeids


def trends_and_volumes(woeid):
    """
    create a dict of trends from a certain woeid, and tweet_volume
    :return: dict
    """
    if args.listoflocations:
        pass
    elif args.woeid:
        woeid = args.woeid
    # else:
    #     woeid = location_to_woeid(args.location)
    trending_topics = []
    tweet_volume = []
    woeid_trends = twitter_api.trends_place(woeid)
    for woeid_trend in woeid_trends:
        for x in range(args.top):
            trending_topics.append(woeid_trend['trends'][x]['name'])
            if woeid_trend['trends'][x]['tweet_volume'] is None:
                woeid_trend['trends'][x]['tweet_volume'] = 0
            tweet_volume.append(woeid_trend['trends'][x]['tweet_volume'])
    tempdict = dict(zip(trending_topics, tweet_volume))
    trend_volume_dict = OrderedDict(sorted(tempdict.items(),
                                    key=lambda t: t[1]))
    items = list(trend_volume_dict.items())
    items.reverse()
    trend_volume_dict = OrderedDict(items)
    print("")
    return trend_volume_dict


def location_to_woeid(location):
    location = location.lower()
    trends = twitter_api.trends_available()
    error_string = "This location cannot be resolved to a WOEID"
    all_woeids = get_woeid_usa()
    if location in all_woeids:
        return all_woeids[location]
    else:
        raise ValueError('This location cannot be resolved to a WOEID')


# def plot_trends():
#     location = args.location
#     trends_plus_volumes = trends_and_volumes(args.woeid)
#     pattern = [Gre, Yel, Red]
#     test = trends_plus_volumes.items()
#     data = vcolor(test, pattern)
#     graph = Pyasciigraph(graphsymbol='*')

#     print("These are the current trends as of {} for {}".format(time,
#                                                                 args.location))
#     for line in graph.graph('Graph of trends from {}'.format(location), data):
#         print(line)


def plot_trends_list(locationlist):
    if args.listoflocations:
        locationlist = list(args.listoflocations)
        for location in locationlist:
            trends_plus_volumes = trends_and_volumes(location_to_woeid(location))
            pattern = [Gre, Yel, Red, Cya]
            chart = trends_plus_volumes.items()
            data = vcolor(chart, pattern)
            graph = Pyasciigraph()
            time = datetime.datetime.now().time()
            for line in graph.graph("These are the current " +
                                    "trends for {} as of {}".format(
                    location.title(), time), data):
                print(line)


def example_tweets(query):
    """
    takes in a trend, and returns 5 tweets that contain that trend
    """
    query = query + " -filter:links"
    tweets = twitter_api.search(query, result_type='popular', lang='en')
    for tweet in tweets:
        print(tweet.text)


def main():
    time = datetime.datetime.now().time()
    woeids = get_woeid_usa()
    if args.listoflocations:
        plot_trends_list(args.listoflocations)
    if args.query:
        example_tweets(args.query)


if __name__ == '__main__':
    main()
