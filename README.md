# Creating a command line interface for Twitter trends

I wanted to come up with a way to quickly discover the trending twitter topics of different regions of the United States (and world) without having to physically going to check each time. For that I decided to write a python program that would do this for me.

Since this is a command line program, I figured using `argparse` to handle command line input. For interacting with Twitter I use the `Tweepy Python Twitter API`. In order to make the data displayed back to me easy to read, I implored the use of `ascii_graph`

## Getting started
First thing you need are twitter api credentials. You can get these by signing up on [dev.twitter.com](https://dev.twitter.com). I won't go into too much detail there since it is fairly easy to google that information and go from there. Starting off with declaring our twitter api as follows:

    import secrets
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    twitter_api = tweepy.API(auth)
    
 I chose to declare my Twitter access_tokens and consumer information in a separate python file since those are not ment to be shared publicly. I can import them into my own program by using `import secrets` (**note**: in this case, 'secrets' must be in the same directory).
 
 ## Trends
 Going off of the [Tweepy API Documentation](http://docs.tweepy.org/en/v3.5.0/) we can get the available trends by using the api method `trends_available()`. We will save that to a variable and then format the information to our liking.
 
    places = twitter_api.trends_available()
    
Taking a look at what we got back from our trends call we can see how the trend locations are formatted

    {'name': 'Worldwide', 'placeType': {'code': 19, 'name': 'Supername'}, 'url': 'http://where.yahooapis.com/v1/place/1', 'parentid': 0, 'country': '', 'woeid': 1, 'countryCode': None}
    
We are only concerned about the `woeid` and the `name` so we can extract only those:

    all_woeids = {place['name'].lower(): place['woeid'] for place in places}
    
We can verify that it works by printing the woeid for philadelphia:

    print(all_woeids['philadelphia'])
    > 2471217
 
## Command Line Args
 Detouring to the command line arguements for a moment, we need to decide what we would like to have as options for our program. I decided on the following command line arguements:
 
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--woeid",
                        help="the woeid of where trends should come from")
    parser.add_argument("-t", "--top", default=10, type=int,
                        help="the number of trends to get: default is 10")
    parser.add_argument('-lol', '--listoflocations', nargs='*',
                        help='a list of locations or a single location')
    parser.add_argument("-q", "--query",
                        help="gives tweets that contain the query")
    args = parser.parse_args()
    
    
## Trends and Volumes
We can pass in woeids of where to get trends from and then we can parse the json response and store them in a dictionary format. I append the topic to one list and the volume to another and then use the `zip()` function to create a `dict` containing the trend and corresponding volume.

Passing in the `-lol` arguement we can run something like `python twitter_news.py -lol Philadelphia Barcelona`


Which will return an `ascii_graph` of the data like so:

[Output](http://imgur.com/a/JglP7)

 
 
