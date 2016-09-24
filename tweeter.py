import twitter
import yaml
import os

def copy_fields(obj, D, fields):
    for field in fields:
        value = getattr(obj, field)
        if type(value)==unicode:
            try:
                value = str(value)
            except UnicodeEncodeError:
                None
        D[field] = value

class Tweeter:
    def __init__(self):
        config_fn = os.path.join( os.path.dirname(__file__), 'config.yaml')
        config = yaml.load(open(config_fn))

        self.api = twitter.Api(consumer_key=config['api_key'],
                          consumer_secret=config['api_secret'],
                          access_token_key=config['token'],
                          access_token_secret=config['token_secret'])
                          
        self.root = config['folder']
        if not os.path.exists(self.root):
            os.mkdir(self.root)
        
        main_fn = os.path.join(self.root, 'tweeter.yaml')
        if os.path.exists(main_fn):
            self.meta = yaml.load(open(main_fn))
        else:
            self.meta = {}
        
        self.lists = {}
        for slug in self.meta.get('lists', []):
            fn = self.get_list_info(slug)
            if os.path.exists(fn):
                D = yaml.load(open(fn))
            else:
                D = {}
            self.lists[slug] = D
            
        self.users = {}
        user_folder = os.path.join(self.root, 'users')
        if not os.path.exists(user_folder):
            os.mkdir(user_folder)
    
    def get_list_info(self, slug):
        return os.path.join(self.root, slug + '.yaml')
        
    def get_user_info(self, handle):
        return os.path.join(self.root, 'users', handle + '.yaml')

    # API METHODS ##############################################################
    def query_lists(self):
        lists = {}
        for t_list in self.api.GetListsList():
            d = {'id': t_list.id, 
                 'name': str(t_list.name), 
                 'member_count': t_list.member_count}
            lists[str(t_list.slug)] = d
        return lists
        
    def get_list_tweets(self, list_id, since_id=None, count=200):
        return self.api.GetListTimeline(list_id=list_id, since_id=since_id, count=count)
        
    # DB METHODS ###############################################################
    def update_lists(self):
        slugs = []
        for slug, info in sorted(self.query_lists().items()):
            if slug in self.lists:
                self.lists[slug].update(info)
            else:
                self.lists[slug] = info
            slugs.append(slug)
        self.meta['lists'] = slugs
        yaml.dump({'lists': slugs}, open(os.path.join(self.root, 'tweeter.yaml'), 'w'))
        
    def get_user(self, handle):
        if handle in self.users:
            return self.users[handle]
            
        fn = self.get_user_info(handle)
        if os.path.exists(fn):
            D = yaml.load(open(fn))
        else:
            D = {}
        self.users[handle] = D
        return D   
        
    def process_user(self, info):
        handle = info.screen_name
        D = self.get_user(handle)
        fields = ['name', 'description', 'followers_count', 'id', 'profile_image_url']
        copy_fields(info, D, fields)

    def clean_tweet(self, obj):
        tweet = {}
        fields = ['created_at', 'id_str', 'retweet_count', 'text']
        copy_fields(obj, tweet, fields)
        for url in obj.urls:
            tweet['text'] = tweet['text'].replace( url.url, url.expanded_url)
        return tweet
            
    def write(self):
        main_fn = os.path.join(self.root, 'tweeter.yaml')
        yaml.dump(self.meta, open(main_fn, 'w'))
        for slug, info in self.lists.iteritems():
            fn = self.get_list_info(slug)
            yaml.dump(info, open(fn, 'w'))
        for handle, info in self.users.iteritems():
            fn = self.get_user_info(handle)
            yaml.dump(info, open(fn, 'w'))
