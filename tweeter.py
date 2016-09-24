import twitter
import yaml
import os

class Tweeter:
    def __init__(self):
        config_fn = os.path.join( os.path.dirname(__file__), 'config.yaml')
        config = yaml.load(open(config_fn))

        self.api = twitter.Api(consumer_key=config['api_key'],
                          consumer_secret=config['api_secret'],
                          access_token_key=config['token'],
                          access_token_secret=config['token_secret'])


