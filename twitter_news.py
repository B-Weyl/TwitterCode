import tweepy
import secrets
import argparse
import datetime
from ascii_graph import Pyasciigraph
import collections
from collections import OrderedDict

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


def plot_trends():
    location = args.location
    trends_plus_volumes = trends_and_volumes(args.woeid)
    test = trends_plus_volumes.items()
    graph = Pyasciigraph()
    print("These are the current trends as of {} for {}".format(time,
                                                                args.location))
    for line in graph.graph('Graph of trends from {}'.format(location), test):
        print(line)


def plot_trends_list(locationlist):
    locationlist = list(args.listoflocations)
    for location in locationlist:
        trends_plus_volumes = trends_and_volumes(location_to_woeid(location))
        chart = trends_plus_volumes.items()
        graph = Pyasciigraph()
        time = datetime.datetime.now().time()
        for line in graph.graph("These are the current " +
                                "trends for {} as of {}".format(
                location.title(), time), chart):
            print(line)


def main():
    time = datetime.datetime.now().time()
    woeids = get_woeid_usa()
    print(plot_trends_list(args.listoflocations))


if __name__ == '__main__':
    main()
