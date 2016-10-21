#!/usr/bin/python

import tweeter
import re

RT_P = 'https://twitter.com/[^/]+/status/\d+'
RETWEET_PATTERN = re.compile(RT_P)
SUBTWEET_PATTERN = re.compile('.*'+RT_P)

patterns = [RETWEET_PATTERN, SUBTWEET_PATTERN]

def format_tweet(tweet):
    return '@%-15s | %s'%(tweet['handle'], tweet['text']) + (' [%d]'%tweet['retweet_count'] if tweet['retweet_count']>0 else '')

if __name__=='__main__':
    twit = tweeter.Tweeter()
    all = twit.all_tweets()
    print len(all)
    for tweet in all:
        for pattern in patterns:
            if pattern.match(tweet['text']):
                break
        else:
            print format_tweet(tweet)
            x = raw_input().strip()
            if len(x)==0:
                twit.mark_as_read(tweet)
            elif x=='q':
                break
    print len(twit.all_tweets())
    twit.write()