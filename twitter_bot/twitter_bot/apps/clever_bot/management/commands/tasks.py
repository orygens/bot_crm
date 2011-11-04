import asyncore 
from clever_bot.models import MentionKeyword, Status, Settings
from account.models import User
from django.core.management.base import NoArgsCommand
import tweepy
from clever_bot.extractors.tweetextractor import TweetExtractor


tweet_extractor = TweetExtractor()


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            print status.text.encode('utf-8')
        except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass


def search_handler(user):
    settings = user.twitter_settings.all()
    if settings.count() == 0:
        settings = Settings()
        settings.last_id = ''
        settings.twitter_account = user
        settings.save()
    else:
        settings = settings[0]

    statuses = Status.objects.filter(twitter_account=user)

    tweets = user.twitter_api._api.mentions(since_id=settings.last_id)
    for tweet in tweets:
        if tweet.text.startswith('@%s' % user.twitter_api.screen_name):
            for status in statuses:
                keywords = [keyword.keyword 
                            for keyword in status.keyword.all() 
                                if keyword.keyword.lower() in tweet.text.lower()]
                if len(keywords) == status.keyword.all().count():
                    sc = tweet.user.screen_name
                    user.twitter_api._api.update_status('@%s %s' % (sc, status.text))
                    break

    if tweets:
        last_id = tweets[0].id
        settings.last_id = last_id
        settings.save()


def streamming_handler(api):
    auth = api._api.auth
    l = StreamListener()
    streamer = tweepy.Stream(auth, l, timeout=3000000000, secure=True)
    streamer.userstream()
    print 'cheguei aqui'

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        user = User.objects.get(username='testeMagazine')
        search_handler(user)








'''

import tweepy
from config import *
from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from models import Author, Tweet, TweetHistory
from core import MonitoreseExtractor
import datetime

ACCESS_KEY = '46898458-3MqYD2T15WIYcNvgF6pRNvfKN9F4PSxjaasErkz3Z'
ACCESS_SECRET = '4GdfLMwx3nGjslJNkiq3bxbH5wl8BJrBE4D5AQ4kU'


def setup_real_twitter(user):
    auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(user.token_key, user.token_secret)
    api = tweepy.API(auth)
    return api, auth


@task
def craw_user_info(author, api):
    me = MonitoreseExtractor(API_KLOUT_KEY, api)
    user_info = me.user_info_api(me.username)

    #Save the Author History
    if author.last_update is not None:
        ah = AuthorHistory()
        ah.date = author.last_update
        ah.author = author
        ah.mentions_quantity = author.mentions_quantity
        ah.listed_quantity = author.listed_quantity
        ah.followers_quantity = author.followers_quantity
        ah.tweet_quantity = author.tweet_quantity
        ah.following_quantity = author.following_quantity
        ah.true_reach = author.true_reach
        ah.save()

    author.last_update = user_info['timestamp']
    author.followers = user_info['followers_ids']
    author.following_quantity = user_info['friends_count']
    author.followers_quantity = user_info['followers_count']
    author.listed_quantity = user_info['listed_count']

    #Updating the true_reach
    tr = me.klout_true_reach(me.username)
    if tr is not None:
        author.true_reach = tr

    author.save()


@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def update_users():
    #Para cada usuario dentro da base que seja ativo a conexao
    #Criar uma nova sub-task para captura de informacoes do Usuario.
    authors = Author.objects.filter(is_active=True)
    for author in authors:
        #Cria uma instancia da api
        api, auth = setup_real_twitter(author)
        #Vamos lancar uma subtask
        craw_user_info.delay(author, api)


@periodic_task(run_every=crontab(hour="23", minute="59", day_of_week="*"))
def update_history():
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    #Para cada tweet dentro da base, temos que guardar o historico dela a cada dia.
    tweets = Tweet.objects.filter(expire__lte=now)
    for tweet in tweets:
        th = TweetHistory()
        th.date = tweet.date
        th.retweet_quantity = tweet.retweet_quantity
        th.reply_quantity = tweet.reply_quantity
        th.tweet = tweet
        th.save()


def activate_streamming(user):
    #Cria uma instancia da api
    api, auth = setup_real_twitter(user)
    #Iniciar monitoramento
    me = MonitoreseExtractor(API_KLOUT_KEY, api)
    streamer = tweepy.Stream(auth, me, timeout=3000000000, secure=True)
    streamer.userstream()

    auth1 = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth1.set_access_token(ACCESS_KEY,  ACCESS_SECRET)
api = tweepy.API(auth1)

l = StreamListener()
streamer = tweepy.Stream(auth1, l, timeout=3000000000, secure=True)
streamer.userstream()

'''

