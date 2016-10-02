#!/usr/bin/python
from flask import Flask, render_template, request, jsonify
import tweeter
app = Flask(__name__)

class Reader:
    def __init__(self):
        self.twit = tweeter.Tweeter()
        self.skipped = set()
        self.current = None
        
    def post(self, read):
        if self.current is None:
            return
        if read:
            self.twit.mark_as_read(self.current)
        else:
            self.skipped.add(self.current['id_str'])
        self.current = None
        
    def get_tweet(self):
        for lname, tweets in self.twit.tweets.iteritems():
            for tweet in tweets:
                if tweet['id_str'] in self.skipped:
                    continue
                else:
                    self.current = tweet
                    return self.current['id_str']

reader = Reader()

@app.route('/')
def index():
    return render_template('tweet.html')

@app.route('/interact')
def interact():
    if 'read' in request.args:
        reader.post(request.args.get('read')=='true')
    id = reader.get_tweet()
    return jsonify(id=id)

if __name__ == '__main__':
    try:
        app.run()
    finally:
        reader.twit.write()
