#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mobility import Mobility

import tweeter
import os.path
import re
app = Flask(__name__)
Mobility(app)

INSTAGRAM_PATTERN = re.compile('https://(?:www\.)?instagram.com/p/([^/]*)/')
WRITE_COUNT = 15


class Reader:
    def __init__(self):
        self.twit = tweeter.Tweeter()
        self.current = None
        self.clear_message = None
        self.count = 0

    def post(self, action):
        if self.current is None:
            return
        self.count += 1
        if action == 'read':
            self.twit.mark_as_read(self.current)
        elif action == 'sleep':
            self.twit.sleep_tweet(self.current)
        else:
            self.twit.skip_tweet(self.current)
        self.current = None

    def mark_all(self, user, mode='fresh'):
        self.twit.mark_all(user, mode=mode)

    def get_tweet(self, chosen_list=None, username=None, mode='fresh', sort='time'):
        tweet = self.twit.get_tweet(chosen_list, username, mode=mode, sort=sort)
        self.current = tweet
        if not self.current:
            return {}
        M = {'id': self.current['id_str']}
        rt = tweet.get('rt', None)
        if rt:
            M['id'] = rt
            M['retweeter'] = tweet['handle']
        if 'id2' in tweet:
            M['id2'] = tweet['id2']
        m = INSTAGRAM_PATTERN.search(tweet['text'] + ' ' + tweet.get('rt_text', ''))
        if m:
            M['extra_img'] = 'https://instagram.com/p/%s/media/?size=m' % m.group(1)
        return M

    def needs_writing(self):
        return self.count >= WRITE_COUNT

    def reset(self):
        self.count = 0

reader = Reader()


@app.route('/')
def index():
    if request.MOBILE:
        return render_template('m_tweet.html')
    return render_template('tweet.html')


@app.route('/interact')
def interact():
    if 'action' in request.args:
        action = request.args.get('action')
        reader.post(action)
    slug = request.args.get('list', 'all')
    username = request.args.get('user', None)
    if slug == 'all':
        slug = None
    if username == 'all':
        username = None
    mode = request.args.get('mode', 'fresh')
    sort = request.args.get('sort', 'time')
    M = reader.get_tweet(slug, username, mode, sort)
    M['lists'] = reader.twit.get_sizes(mode)
    if slug:
        M['users'] = sorted(reader.twit.get_user_counts(slug, mode).items())
    if reader.clear_message is not None:
        if reader.clear_message == 0:
            reader.clear_message = None
            M['message'] = ' '
        else:
            reader.clear_message -= 1
    if reader.needs_writing():
        reader.twit.write()
        reader.reset()
    return jsonify(M)


@app.route('/tweeter.css')
def css():
    return render_template('tweeter.css')

@app.route('/mobile.css')
def css2():
    return render_template('mobile.css')

@app.route('/formatted')
def format_tweet():
    J = dict(reader.current)
    J.update(reader.twit.get_user(J['handle']))
    return jsonify({'html': render_template('single_tweet.html', data=J)})
    
@app.route('/format')
def format_tweetx():
    J = dict(reader.current)
    J.update(reader.twit.get_user(J['handle']))
    return """<link href="https://fonts.googleapis.com/css?family=Roboto+Condensed" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="mobile.css">""" + render_template('single_tweet.html', data=J)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/update')
def update():
    reader.twit.get_tweets()
    reader.clear_message = 5
    return jsonify({'message': 'Updated!'})


@app.route('/write')
def save():
    reader.twit.write()
    reader.clear_message = 5
    return jsonify({'message': 'Written!'})


@app.route('/clear')
def clear():
    n = reader.twit.clear_skips()
    reader.clear_message = 5
    return jsonify({'message': 'Cleared %d!' % n})


@app.route('/mark')
def mark():
    user = request.args.get('user')
    mode = request.args.get('mode', 'fresh')
    reader.mark_all(user=user, mode=mode)
    return jsonify({})

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
