"""
@anazard
Algorithm based on Adil Moujahid's post (http://adilmoujahid.com/posts/2014/07/twitter-analytics/)
for my AI course at university.
Fill in the constants with your Twitter app credentials.
"""

from twython import Twython, TwythonError
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import json

# The blocks below require internet connection to work, so I previously stored a copy
# of my own timeline object so that I can use when no connection is available

# Twitter authentication constants
ACCESS_TOKEN        = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY        = ""
CONSUMER_KEY_SECRET = ""

# Twython object
twitter = Twython(CONSUMER_KEY, CONSUMER_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Grabs data from my timeline
try:
    timeline = twitter.get_home_timeline(screen_name='anazard')
except TwythonError as e:
    print e

# Prints it out
# print timeline

# Shows the amount of tweets retrieved
# print len(timeline)

# Stores the timeline info (for offline use)
with open('timeline.pkl', 'wb') as f:
    pickle.dump(timeline, f, pickle.HIGHEST_PROTOCOL)

# Restores the timeline object
with open('timeline.pkl', 'rb') as f:
    timeline = pickle.load(f)

# Creates a new data frame
tweets = pd.DataFrame()

# Prepares the data and assigns it to a key from the data frame
tweets['lang']   = map(lambda tweet: tweet['lang'], timeline)
tweets['place']  = map(lambda tweet: tweet['user']['location'] if tweet['user']['location'] != None else None, timeline)

# Generates and opens up a bar chart with the information provided
def generate_chart(data, x_label, y_label, title, color='blue'):
    tweets = data.value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label , fontsize=15)
    ax.set_title(title, fontsize=15, fontweight='bold')
    tweets[:5].plot(ax=ax, kind='bar', color=color)
    fig.subplots_adjust(bottom=0.5)
    plt.show(block=True)

# Does the magic by calling new charts
generate_chart(tweets['place'], '# of tweets', 'Place', 'Where are my friends tweeting from?')
generate_chart(tweets['lang'], '# of tweets', 'Languages', 'Languages on my timeline')
