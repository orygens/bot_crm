#-*-coding:utf-8-*-

import os.path
from django.utils import simplejson
from nose.tools import assert_raises, assert_equals

from ..basictokenizer import BasicTokenizer
from ..tweettokenizer import TweetTokenizer
from ..urlextractor import extract_url_info
from ..tweetextractor import TweetExtractor
from ..utils import fix_date_format

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))


def test_tokenize_empty_strings():
    text = ""
    tokenizer = BasicTokenizer()
    assert_equals([],tokenizer.tokenize(text))
    tokenizer = TweetTokenizer()
    assert_equals([],tokenizer.tokenize(text))


def test_tokenize_simple_strings():
    text_one = u"Foto em 180º da fila para a #WWDC: RT @razorianfly: http://t.co/o9xF27i (via @GeekAndrew)"
    
    text_two = u"LOL RT @jkendrick: I'm feeling better about everything already, and nothing's happened yet #wwdc"
    
    text_three = u"todos convidados para participar do bolão dos rumores dos anúncios da Apple; no WWDC ;-) http://br-mac.org/?p=790"
    
    text_four = u"O Brasil é o 1o. Lugar no ranking dos países com potencial de atrair investimentos para o Varejo http://bit.ly/jneuh9 via @falandodevarejo"
    
    text_five = u"RT @radarCITi: Parabéns @FCAPJR, @aceconsultoria e @ProdutivaJr pelos cases vencedores do Destine. A @fejepe mais uma vez mostra sua força!"

    tokenizer = BasicTokenizer()
    tokenizer_t = TweetTokenizer()

    assert_equals(['Foto', 'em', '180', 'da', 'fila', 'para', 'a', 'WWDC', 'RT', 'razorianfly', 'http', 't', 'co', 'o9xF27i', 'via', 'GeekAndrew'],tokenizer.tokenize(text_one))
    assert_equals([('WORD', u'Foto'), ('WORD', u'em'), ('WORD', u'180\xba'), ('WORD', u'da'), ('WORD', u'fila'), ('WORD', u'para'), ('WORD', u'a'), 
                   ('#TAG', u'#WWDC'), ('COLON', u':'), ('RT', u'RT'), ('@NAME', u'@razorianfly'), ('COLON', u':'), ('URL', u'http://t.co/o9xF27i'), 
                   ('LEFT_PAREN', u'('), ('WORD', u'via'), ('@NAME', u'@GeekAndrew'), ('RIGHT_PAREN', u')')],tokenizer_t.tokenize(text_one))

    assert_equals(['LOL', 'RT', 'jkendrick', 'I', 'm', 'feeling', 'better', 'about', 'everything', 'already', 'and', 'nothing', 's', 'happened', 'yet', 'wwdc'],tokenizer.tokenize(text_two))
    assert_equals([('WORD', 'LOL'), ('RT', 'RT'), ('@NAME', '@jkendrick'), ('COLON', ':'), ('WORD', "I'm"), ('WORD', 'feeling'), 
                   ('WORD', 'better'), ('WORD', 'about'), ('WORD', 'everything'), ('WORD', 'already'), ('COMMA', ','), ('WORD', 'and'), 
                   ('WORD', "nothing's"), ('WORD', 'happened'), ('WORD', 'yet'), ('#TAG', '#wwdc')],tokenizer_t.tokenize(text_two))

    assert_equals(['todos', 'convidados', 'para', 'participar', 'do', 'bol', 'o', 'dos', 'rumores', 'dos', 'an', 'ncios', 'da', 'Apple', 'no',
                  'WWDC', 'http', 'br', 'mac', 'org', 'p', '790'], tokenizer.tokenize(text_three))
    assert_equals([('WORD', u'todos'), ('WORD', u'convidados'), ('WORD', u'para'), ('WORD', u'participar'), ('WORD', u'do'), ('WORD', u'bol\xe3o'), ('WORD', u'dos'), 
                   ('WORD', u'rumores'), ('WORD', u'dos'), ('WORD', u'an\xfancios'), ('WORD', u'da'), ('WORD', u'Apple'), 
                   ('OTHER', u';'), ('WORD', u'no'), ('WORD', u'WWDC'), ('EMOTICON', u';-)'), ('URL', u'http://br-mac.org/?p=790')],tokenizer_t.tokenize(text_three))

    assert_equals(['O', 'Brasil', 'o', '1o', 'Lugar', 'no', 'ranking', 'dos', 'pa', 'ses', 'com', 'potencial', 'de', 'atrair', 'investimentos', 'para', 'o', 
                   'Varejo', 'http', 'bit', 'ly', 'jneuh9', 'via', 'falandodevarejo'],tokenizer.tokenize(text_four))
    assert_equals([('WORD', u'O'), ('WORD', u'Brasil'), ('WORD', u'\xe9'), ('WORD', u'o'), ('WORD', u'1o'), ('DOTS', u'.'), 
                   ('WORD', u'Lugar'), ('WORD', u'no'), ('WORD', u'ranking'), ('WORD', u'dos'), ('WORD', u'pa\xedses'), 
                   ('WORD', u'com'), ('WORD', u'potencial'), ('WORD', u'de'), ('WORD', u'atrair'), ('WORD', u'investimentos'),
                   ('WORD', u'para'), ('WORD', u'o'), ('WORD', u'Varejo'), ('URL', u'http://bit.ly/jneuh9'), ('WORD', u'via'), 
                   ('@NAME', u'@falandodevarejo')],tokenizer_t.tokenize(text_four))

    assert_equals(['RT', 'radarCITi', 'Parab', 'ns', 'FCAPJR', 'aceconsultoria', 'e', 'ProdutivaJr', 'pelos', 'cases', 'vencedores', 'do', 
                   'Destine', 'A', 'fejepe', 'mais', 'uma', 'vez', 'mostra', 'sua', 'for', 'a'],tokenizer.tokenize(text_five))
    assert_equals([('RT', u'RT'), ('@NAME', u'@radarCITi'), ('COLON', u':'), ('WORD', u'Parab\xe9ns'),
                  ('@NAME', u'@FCAPJR'), ('COMMA', u','), ('@NAME', u'@aceconsultoria'),
                   ('WORD', u'e'), ('@NAME', u'@ProdutivaJr'), ('WORD', u'pelos'), ('WORD', u'cases'),
                   ('WORD', u'vencedores'), ('WORD', u'do'), ('WORD', u'Destine'), ('DOTS', u'.'), ('WORD', u'A'), 
                   ('@NAME', u'@fejepe'), ('WORD', u'mais'), ('WORD', u'uma'), ('WORD', u'vez'), ('WORD', u'mostra'), 
                   ('WORD', u'sua'), ('WORD', u'for\xe7a'), ('EXCLAIM', u'!')],tokenizer_t.tokenize(text_five))


def test_unshorten_urls():
    url = 'http://www.google.com'
    url_2 =  'url_invalida'
    url_3 = 'http://bit.ly/jneuh9'
    url_4 = 'http://bit.ly/ijdijddijd'
    url_5 = 'https://pagseguro.uol.com.br/#rmcl'
    
    assert_equals({'url': 'http://www.google.com.br/', 'title': u'Google'},extract_url_info(url))
    assert_equals({'url': 'url_invalida', 'title': ''},extract_url_info(url_2))
    assert_equals({'url': 'http://falandodevarejo.blogspot.com/2011/06/varejo-brasileiro-ja-atrai-mais-que-o.html', 
                   'title': u'FALANDO DE VAREJO - O blog do varejo brasileiro: Varejo brasileiro j\xe1 atrai mais que o chin\xeas'}
                 ,extract_url_info(url_3))
    assert_equals({'url': 'http://bit.ly/ijdijddijd', 'title': u''} ,extract_url_info(url_4))   
    assert_equals({'url': 'https://pagseguro.uol.com.br/', 'title': u'PagSeguro &ndash; A solu\xe7\xe3o completa para pagamentos online'},extract_url_info(url_5))


def test_extract_tweets():
    extractor = TweetExtractor()
    tweets_input = open(PROJECT_ROOT +'/search_results.json')
    tweets_input =  simplejson.loads(tweets_input.read())
    for index,tweet in enumerate(tweets_input):
           print extractor.RT(tweet)
           print extractor.text(tweet).encode('utf-8')
           print extractor.createdAt(tweet)
           print extractor.profile_img_url(tweet)
           print extractor.location(tweet)
           print extractor.verified(tweet)
           print extractor.statuses_count(tweet)
           print extractor.listed_count(tweet)
           print extractor.followers_count(tweet)
           print extractor.friends_count(tweet)
           print extractor.geo(tweet)
           print extractor.id(tweet)
           print extractor.user_id(tweet)
           print extractor.user_name(tweet)


def setup_real_twitter():
  username = ''
  import tweepy
  
  CONSUMER_KEY = ''
  CONSUMER_SECRET = ''
  ACCESS_KEY = '46898458-3MqYD2T15WIYcNvgF6pRNvfKN9F4PSxjaasErkz3Z'
  ACCESS_SECRET = '4GdfLMwx3nGjslJNkiq3bxbH5wl8BJrBE4D5AQ4kU'

  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
  api = tweepy.API(auth)
  return api

def test_extract_mentions():
  extractor = TweetExtractor()
  tweets_input = open(PROJECT_ROOT +'/mentions_results.json')
  tweets_input =  simplejson.loads(tweets_input.read())
  for index,tweet in enumerate(tweets_input):
      print tweet['text'].encode('utf-8')
      print extractor.check_mention(tweet,'rafaelcaricio')
      print extractor.check_mention(tweet,'orygens')


