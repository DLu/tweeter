#!/usr/bin/python

import tweeter
import pprint

twit = tweeter.Tweeter()
ext = 0
rec = 0
for tweet in twit.all_tweets():
    if tweeter.needs_extension(tweet['text']):
        t2 = twit.clean_tweet(twit.get_extended_status(tweet['id_str']))
        tweet.update(t2)
        ext+=1
    if (tweeter.is_retweet(tweet) and 'rt' not in tweet) or \
        (tweeter.is_subtweet(tweet) and 'id2' not in tweet):
        twit.recurse(tweet)
        rec+=1

twit.write()
print '%d extensions, %d recursions'%(ext, rec)