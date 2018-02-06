#!/usr/bin/python

import tweeter
import collections

twit = tweeter.Tweeter()

users = collections.OrderedDict()

for friend in twit.api.GetFriends(skip_status=True):
    D = friend.AsDict()
    users[D['screen_name']] = D

for t_list in twit.api.GetListsList():
    for member in twit.api.GetListMembers(list_id=t_list.id, skip_status=True):
        name = member.screen_name
        if name in users:
            del users[name]

for username, d in users.iteritems():
    s = '%s: %s - %s' % (username, d.get('name', ''), d.get('description', ''))
    print s
    print '='*len(s)
    for i, list in enumerate(twit.ordered_lists):
        print '%d) %s' % (i, list)
    x = raw_input('? ')
    if x == 'q':
        exit(0)
    try:
        index = int(x)
        list = twit.ordered_lists[index]
    except:
        print 'Error'
        continue
    twit.api.CreateListsMember(list_id=twit.lists[list]['id'], screen_name=username)
    print 'Yay!'
