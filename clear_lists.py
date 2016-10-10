#!/usr/bin/python

import tweeter

twit = tweeter.Tweeter()

while True:
    for i, (name, size) in enumerate(twit.get_sizes()):
        print '%02d) %-12s %4s'%(i, name, str(size))
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