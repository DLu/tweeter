#!/usr/bin/python

import tweeter
import pprint

twit = tweeter.Tweeter()
ext, rec = twit.fix_up_tweets()
twit.write()
print '%d extensions, %d recursions'%(ext, rec)