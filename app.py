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
        
    def get_tweet(self, chosen_list=None):
        tweet = self.twit.get_tweet(chosen_list, self.skipped)
        self.current = tweet
        if self.current:
            return self.current['id_str']

reader = Reader()

@app.route('/')
def index():
    return render_template('tweet.html')

@app.route('/interact')
def interact():
    if 'read' in request.args:
        reader.post(request.args.get('read')=='true')
    slug = request.args.get('list', 'all')
    if slug=='all':
        slug = None
    id = reader.get_tweet(slug)
    M = {'id': id, 'lists': reader.twit.get_sizes()}
    return jsonify(M)
    
@app.route('/tweeter.css')
def css():
    return render_template('tweeter.css')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0')
    finally:
        reader.twit.write()
