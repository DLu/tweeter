#!/usr/bin/python

import tweeter

twit = tweeter.Tweeter()

while True:
    for i, (name, info) in enumerate(twit.lists.iteritems()):
        print '%02d) %-12s %4s'%(i, name, str(len(twit.tweets[name])))
    inp = raw_input('clear list? ')
    if inp=='q':
        break
    try:
        index = int(inp)
        key = twit.lists.keys()[index]
        twit.clear_tweets(key)
    except:
        continue
    print 

twit.write()