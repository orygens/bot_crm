# -*- coding: utf-8 -*-

import random
import tweepy
from django.contrib.auth.models import User
from tweepy.models import Status as Tweet
from django.core.management.base import BaseCommand
from clever_bot.models import Status, DefaultAnswer
import json

CONSUMER_KEY = 'A6uwpIhHkO3tnbR7UwYZ8w'
CONSUMER_SECRET = 'SCjpCmrg3Apj2tvpiPB2aigMeZYr5xJSLStDfK2a5dg'
ACCESS_KEY = '404297121-izjPGD8IhjWEmBif6VGyGW3RpsmVP4h7qGtgpllA'
ACCESS_SECRET = 'j49OFFzf6YuP7rSdFpN6zWr4e9Kuol2Fe1fSJxtwg'


class StreamListener(tweepy.StreamListener):
    def on_error(self, status):
        print status
        return False

    def on_data(self, data):
        if 'entities' in data:
            data = json.loads(data)
            user_mentions = data['entities']['user_mentions']
            screen_names = [mention['screen_name'] \
                        for mention in user_mentions]
            if 'testeMagazine' in screen_names:
                status = Tweet.parse(self.api, data)
                self.on_mention(status)

    def on_mention(self, status):
        try:
            user = User.objects.get(username='testeMagazine')
            statuses = Status.objects.filter(twitter_account=user)

            for s in statuses:
                keywords = [keyword.keyword for keyword in s.keyword.all()\
                    if keyword.keyword.lower() in status.text.lower()]

                if len(keywords) == s.keyword.count():
                    try:
                        user.twitter_api._api.update_status(
                            '@%s %s' % (status.user.screen_name, s.text),
                           in_reply_to_status_id=status.id
                        )
                    except:
                        try:
                            user.twitter_api._api.update_status(
                                'Olá @%s, %s' % (status.user.screen_name, s.text),
                               in_reply_to_status_id=status.id
                            )
                        except:
                            user.twitter_api._api.update_status(
                                'Oi @%s, %s' % (status.user.screen_name, s.text),
                               in_reply_to_status_id=status.id
                            )
                    break
            else:
                d_statuses = DefaultAnswer.objects.all()
                if d_statuses.count() > 0:
                    try:
                        d_statuses = [d_status.text for d_status in d_statuses]
                        user.twitter_api._api.update_status(
                            '@%s %s' % (status.user.screen_name, random.choice(d_statuses)),
                           in_reply_to_status_id=status.id
                        )
                    except:
                        d_statuses = [d_status.text for d_status in d_statuses]
                        user.twitter_api._api.update_status(
                            'Olá @%s, %s' % (status.user.screen_name, random.choice(d_statuses)),
                           in_reply_to_status_id=status.id
                        )

            print status.text.encode('utf-8')
        except UnicodeDecodeError, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        auth1 = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth1.set_access_token(ACCESS_KEY,  ACCESS_SECRET)
        api = tweepy.API(auth1)
        l = StreamListener()
        streamer = tweepy.Stream(auth1, l, timeout=3000000000, secure=True)
        streamer.userstream()
        print 'Streamer Activaded!'
