#-*- coding:utf-8 -*-

"""

Copyright (c) 2010 Monitore.se
marcel@orygens.com

"""

import sys
import datetime
from re import search, split
from tweettokenizer import *
from urlextractor import unshortenURL, extract_url_info
from utils import fix_date_format


class TweetExtractor(object):
    '''
    This class is the Twitter Extractor, which is responsable of:
        1. Extract the text of the tweet.

        2.urls. A list of any urls in the tweet

        3.hashtags. List of hashtags with the tweet in the order that they appeared

        4.@names. List of @names in the tweet in order that they appeared.

        Structure:

        {'text': 'text',
         'links': ['link1','link2','link3'],
         'tags':['#hash1', '#hash2'],
         'mentions':['username1','username2'],
         'RT':False,
         'Created_at': '23/04/2010 00:34:00 AM',
         'geo':None,
         'location': 'Recife, Pernambuco',
         'username': 'name',
         'id': 30303,
         'user_id': 30404}

    The tokens can then be further processed with the Keyword Tagger for example.
    '''
    
    tweetTokenizer = TweetTokenizer()

    @staticmethod
    def text(tweet):
        '''
        Returns
        --------
        Returns the text of the tweet.
        '''
        return tweet['text']

    @staticmethod
    def createdAt(tweet):
        '''
        Returns
        --------
        Returns the creation date of the tweet.
        '''
        return fix_date_format(tweet['created_at'])

    @staticmethod
    def profile_img_url(tweet):
        '''
        Returns
        --------
        Returns the profile image url of the tweet.
        '''
        return tweet['profile_image_url']

    @staticmethod
    def location(tweet):
        '''
        Returns
        --------
        Returns the location of the tweet.
        '''
        return tweet['user'].get('location',None) if tweet.get('user',None) else None 

    @staticmethod
    def verified(tweet):
        '''
        Returns
        --------
        Returns if the user is verified.
        '''
        return tweet['user'].get('verified',None) if tweet.get('user',None) else None 

    @staticmethod
    def statuses_count(tweet):
        '''
        Returns
        --------
        Returns the number of statuses posted by the user.
        '''
        return tweet['user'].get('statuses_count',None) if tweet.get('user',None) else None 
    
    @staticmethod
    def listed_count(tweet):
        '''
        Returns
        --------
        Returns the number of the lists that the user is counted.
        '''
        return tweet['user'].get('listed_count',None) if tweet.get('user',None) else None 

    @staticmethod
    def followers_count(tweet):
        '''
        Returns
        --------
        Returns the number of followers of the user.
        '''
        return tweet['user'].get('followers_count',None) if tweet.get('user',None) else None 

    @staticmethod
    def friends_count(tweet):
        '''
        Returns
        --------
        Returns the number of friends.
        '''
        return tweet['user'].get('friends_count',None) if tweet.get('user',None) else None 

    @staticmethod
    def geo(tweet):
        '''
        Returns
        --------
        Returns the geolocalization of the tweet.
        '''
        return tweet.get('geo',None)

    @staticmethod
    def id(tweet):
        '''
        Returns
        --------
        Returns the id of the tweet.
        '''
        return tweet['id']

    @staticmethod
    def user_id(tweet):
        '''
        Returns
        --------
        Returns the id of the author.
        '''
        if tweet.has_key('from_user_id'):
            return tweet['from_user_id']
        else:
            return tweet['user']['id']

    @staticmethod
    def user_name(tweet):
        '''
        Returns
        --------
        Returns the username of the author.
        '''
        if tweet.has_key('from_user'):
            return tweet['from_user']
        else:
            return tweet['user']['screen_name']

    @staticmethod
    def urls(tweet):
        '''
        Returns
        --------
        Returns the urls (unshorten) in the tweet.
        '''
        return [unshortenURL(token[1]) for token in\
                 TweetExtractor.tweetTokenizer.tokenize(tweet['text'])\
                 if token[0] == 'URL']

    @staticmethod
    def urls_info(tweet):
        '''
        Returns
        --------
        Returns the titles of the urls in the tweet.
        '''
        return [extract_url_info(token[1]) for token in\
                 TweetExtractor.tweetTokenizer.tokenize(tweet['text'])\
                 if token[0] == 'URL']

    @staticmethod
    def shorten_urls(tweet):
        '''
        Returns
        --------
        Returns the shorten urls in the tweet.
        '''
        return [token[1] for token in\
                 TweetExtractor.tweetTokenizer.tokenize(tweet['text'])\
                 if token[0] == 'URL']

    @staticmethod
    def mentions(tweet):
        '''
        Returns
        --------
        Returns the mentions of the tweet.
        '''
        return [token[1] for token in\
                TweetExtractor.tweetTokenizer.tokenize(tweet['text']) if\
                token[0] == '@NAME']

    @staticmethod
    def check_mention(tweet,username):
        '''
        Returns
        --------
        Returns if mention the username
        '''
        if '@%s' % username in  tweet['text']:
            if tweet.get('in_reply_to_status_id',None) or \
              tweet.get('in_reply_screen_name',None) or tweet.get('in_reply_to_user_id',None)  :
                return {'mention': True, 
                   'replier': TweetExtractor.user_name(tweet), \
                   'type': 'username', 
                   'in_reply_to_status_id': tweet.get('in_reply_to_status_id',None),
                   'in_reply_to_screen_name': tweet.get('in_reply_screen_name',None),
                   'in_reply_to_user_id': tweet.get('in_reply_to_user_id',None)}
        return {'mention': False, 'replier': None, 'type':None}


    @staticmethod
    def RT(tweet):
        '''
        Returns
        --------
        Returns the username of the author.
        '''
        results = search(r'(RT|retweet|from|via)((?:\b\W*@\w+)+)',tweet['text'])
        if results:
            authors = [ word for word in re.findall(r'@(\w+)',results.group(2))]
            return {'RT': True, 'authors': authors}
        else:
            if [token[1] for token in TweetExtractor.tweetTokenizer.tokenize(tweet['text'])\
                     if token[0] == 'RT']:
                return {'RT': True, 'authors':[]}
            return {'RT': False, 'authors':[]}

    @staticmethod
    def hashtags(tweet):
        '''
        Returns
        --------
        Returns the hashtags in the tweet.
        '''
        return [token[1] for token in\
                 TweetExtractor.tweetTokenizer.tokenize(tweet['text'])\
                 if token[0] == '#TAG']
