#!/usr/bin/python

import tweeter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lists', action='store_true')
args = parser.parse_args()

twit = tweeter.Tweeter()
if args.lists:
    twit.update_lists()

twit.write()