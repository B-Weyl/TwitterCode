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


def get_woeids():
    """
    make a dict of woeids and location names
    """
    places = twitter_api.trends_available()
    all_woeids = {place['name'].lower(): place['woeid'] for place in places}
    # store the woeid in a dictionary with its correspoding name
    return all_woeids


def trends_and_volumes(woeid):
    """
    create a dict of trends from a certain woeid, and tweet_volume
    :return: dict
    """
    if args.woeid:
        woeid = args.woeid
    trending_topics = []
    tweet_volume = []
    woeid_trends = twitter_api.trends_place(woeid)
    for woeid_trend in woeid_trends:
        for x in range(args.top):
            trending_topics.append(woeid_trend['trends'][x]['name'])
            # if the trend volume is none, replace it with 0
            # so that graphing the trend is easier
            if woeid_trend['trends'][x]['tweet_volume'] is None:
                woeid_trend['trends'][x]['tweet_volume'] = 0
            tweet_volume.append(woeid_trend['trends'][x]['tweet_volume'])
    tempdict = dict(zip(trending_topics, tweet_volume))
    trend_volume_dict = OrderedDict(sorted(tempdict.items(),
                                    key=lambda t: t[1]))
    items = list(trend_volume_dict.items())
    items.reverse()
    trend_volume_dict = OrderedDict(items)
    return trend_volume_dict


def location_to_woeid(location):
    """
    if user inputs a location instead of woeid
    translate that location to a valid woeid (if there is one)
    """
    location = location.lower()
    trends = twitter_api.trends_available()
    all_woeids = get_woeids()
    if location in all_woeids:
        return all_woeids[location]
    else:
        # The location provided does not match any of the locations
        # available for trends from Twitter
        raise ValueError('This location cannot be resolved to a WOEID')


def plot_trends_list(locationlist):
    """
    create a graph of trends and trend volumes, sorted by trend volume
    """
    if args.listoflocations:
        locationlist = list(args.listoflocations)
        for loc in locationlist:
            trends_plus_volumes = trends_and_volumes(location_to_woeid(loc))
            pattern = [Gre, Yel, Red, Cya]
            chart = trends_plus_volumes.items()
            data = vcolor(chart, pattern)
            graph = Pyasciigraph()
            time = datetime.datetime.now().time()
            for line in graph.graph("These are the current " +
                                    "trends for {} as of {}".format(
                    loc.title(), time), data):
                print(line)


def query_tweets(query):
    """
    takes in a trend, and returns 5 popular tweets that contain that query
    """
    # we don't want tweets with links, it looks nicer this way
    query = query + " -filter:links"
    tweets = twitter_api.search(query, result_type='popular',
                                lang='en', count=5)
    if len(tweets) == 0:
        print("There are no tweets that match your query, " +
              "please try another query")
    for tweet in tweets:
        print(tweet.text)


def main():
    time = datetime.datetime.now().time()
    woeids = get_woeids()
    if args.listoflocations:
        plot_trends_list(args.listoflocations)
    if args.query:
        query_tweets(args.query)


if __name__ == '__main__':
    main()
