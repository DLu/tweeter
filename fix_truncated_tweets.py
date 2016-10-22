#!/usr/bin/python

import tweeter

twit = tweeter.Tweeter()
for tweet in twit.all_tweets():
    if not tweeter.needs_extension(tweet['text']):
        continue
    
    s = twit.get_extended_status(tweet['id_str'])
    t2 = twit.clean_tweet(s)
    
    for k in set(t2.keys() + tweet.keys()):
        print k
        a = tweet.get(k, '')
        b = t2.get(k, '')
        print a
        if a!=b:
            print b
        print
    tweet.update(t2)
    break

twit.write()

