

from lib.tweepy.auth import *

if __name__ == '__main__':
	CONSUMER_KEY = 'EIhqgw5kylzcsQKapalIiw'
	CONSUMER_SECRET = 'rcrzyNr1SnSLLaRnTGF9kkvnEq2VcbP5J3Mx4ZhsU'

	handler = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
	auth_url = handler.get_authorization_url()
	print 'Please authorize:' + auth_url
	verifier = raw_input('PIN: ').strip()
	handler.get_access_token(verifier)
	print "ACCESS_KEY = '%s'" % handler.access_token.key
	print "ACCESS_SECRET = '%s'" % handler.access_token.secret