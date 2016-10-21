#!/usr/bin/python

import tweeter

def should_skip(tweet):
    return tweeter.is_retweet(tweet) or tweeter.is_subtweet(tweet)

def format_tweet(tweet):
    return '@%-15s | %s'%(tweet['handle'], tweet['text']) + (' [%d]'%tweet['retweet_count'] if tweet['retweet_count']>0 else '')

if __name__=='__main__':
    twit = tweeter.Tweeter()
    all = twit.all_tweets()
    print len(all)
    for tweet in all:
        if should_skip(tweet):
            continue
        print format_tweet(tweet)
        x = raw_input().strip()
        if len(x)==0:
            twit.mark_as_read(tweet)
        elif x=='q':
            break
    print len(twit.all_tweets())
    twit.write()