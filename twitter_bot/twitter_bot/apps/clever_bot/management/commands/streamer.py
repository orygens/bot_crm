import tweepy

CONSUMER_KEY = 'A6uwpIhHkO3tnbR7UwYZ8w'
CONSUMER_SECRET = 'SCjpCmrg3Apj2tvpiPB2aigMeZYr5xJSLStDfK2a5dg'
ACCESS_KEY = '404297121-izjPGD8IhjWEmBif6VGyGW3RpsmVP4h7qGtgpllA'
ACCESS_SECRET = 'j49OFFzf6YuP7rSdFpN6zWr4e9Kuol2Fe1fSJxtwg'


class StreamListener(tweepy.StreamListener):


    def on_error(self, status):
        print status
        return False

    def on_status(self, status):
        try:
            print status.text.encode('utf-8')
        except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

auth1 = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth1.set_access_token(ACCESS_KEY,  ACCESS_SECRET)
api = tweepy.API(auth1)
print dir(auth1)
l = StreamListener()
streamer = tweepy.Stream(auth1, l, timeout=3000000000, secure=True)
streamer.userstream()
print 'cheguei aqui!'