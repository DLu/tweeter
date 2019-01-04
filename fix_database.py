#!/usr/bin/python

import tweeter

twit = tweeter.Tweeter()
try:
    twit.fix_up_tweets()
finally:
    twit.write()
