#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, send_from_directory
import tweeter
import os.path
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
        if not self.current:
            return {}
        M = {'id': self.current['id_str']}
        rt = tweeter.is_retweet(tweet)
        if rt:
            M['id'] = rt
            M['retweeter'] = tweet['handle']
        return M

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
    M = reader.get_tweet(slug)
    M['lists'] = reader.twit.get_sizes()
    return jsonify(M)
    
@app.route('/tweeter.css')
def css():
    return render_template('tweeter.css')

@app.route('/formatted')
def format_tweet():
    J = dict(reader.current)
    J.update(reader.twit.get_user(J['handle']))
    return jsonify({'html': render_template('single_tweet.html', data=J)})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
    
@app.route('/update')
def update():
    reader.twit.get_tweets()
    return jsonify({'message': 'Updated!'})

@app.route('/write')
def save():
    reader.twit.write()
    return jsonify({'message': 'Written!'})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0')
    finally:
        reader.twit.write()
