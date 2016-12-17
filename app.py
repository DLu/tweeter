#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, send_from_directory
import tweeter
import os.path
import re
app = Flask(__name__)

INSTAGRAM_PATTERN = re.compile('https://instagram.com/p/([^/]*)/')

class Reader:
    def __init__(self):
        self.twit = tweeter.Tweeter()
        self.current = None
        
    def post(self, read):
        if self.current is None:
            return
        if read:
            self.twit.mark_as_read(self.current)
        else:
            self.twit.skip_tweet(self.current)
        self.current = None
        
    def mark_all(self, user):
        self.twit.mark_all(user)
        
    def get_tweet(self, chosen_list=None, username=None, include_retweets=False):
        tweet = self.twit.get_tweet(chosen_list, username, include_retweets=include_retweets)
        self.current = tweet
        if not self.current:
            return {}
        M = {'id': self.current['id_str']}
        rt = tweeter.is_retweet(tweet)
        if rt:
            M['id'] = rt
            M['retweeter'] = tweet['handle']
        else:
            st = tweeter.is_subtweet(tweet)
            if st:
                M['id2'] = st        
        m = INSTAGRAM_PATTERN.search(tweet['text'])
        if m:
            M['extra_img'] = 'https://instagram.com/p/%s/media/?size=m'%m.group(1)
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
    username = request.args.get('user', None)
    if slug=='all':
        slug = None
    if username=='all':
        username = None
    rt = request.args.get('rt', False)=='true'
    M = reader.get_tweet(slug, username, rt)
    M['lists'] = reader.twit.get_sizes()
    if slug:
        M['users'] = sorted(reader.twit.get_user_counts(slug).items())
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

@app.route('/clear')
def clear():
    n = reader.twit.clear_skips()
    return jsonify({'message': 'Cleared %d!'%n})

@app.route('/mark')
def mark():
    user = request.args.get('user')
    reader.mark_all(user=user)
    return jsonify({})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0')
    finally:
        reader.twit.write()
