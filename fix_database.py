#!/usr/bin/python

import tweeter
import pprint

twit = tweeter.Tweeter()
twit.fix_up_tweets()
twit.write()
