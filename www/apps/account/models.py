# -*- coding: utf-8 -*-

import re
import tweepy
from django.conf import settings
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth

class UserTweepyExtension(object):
    @property
    def twitter_api(self):
        if not hasattr(self, '_twitter_api'):
            self._twitter_api = None

        if not self._twitter_api:
            social_auth = UserSocialAuth.objects.get(user=self, provider='twitter')
            oauth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                settings.TWITTER_CONSUMER_SECRET)
            matches = re.search(r'oauth_token_secret=(?P<secret>[\w\d-]*)&' +\
                r'oauth_token=(?P<key>[\w\d-]*)',
                social_auth.extra_data['access_token'])
            group_dict = matches.groupdict()
            oauth.set_access_token(group_dict['key'], group_dict['secret'])
            self._twitter_api = tweepy.API(oauth).me()

        return self._twitter_api

User.__bases__ += (UserTweepyExtension,)
