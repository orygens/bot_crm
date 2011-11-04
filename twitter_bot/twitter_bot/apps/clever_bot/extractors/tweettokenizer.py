#-*- coding:utf-8 -*-

"""

Copyright (c) 2010 Monitore.se
marcel@orygens.com

"""

import re
import sys
from utils import TokenizerException

class TweetTokenizer(object):
    '''
    
    This class is the Twitter Tokenizer, which is responsable of:
    1. Parse and Tokenize the essential structure from the tweet's text

    The tokens can then be further processed with the Keyword Tagger for example.   
    
    Parameters
    -----------
    text : string  Text that will be tokenized.
    
    Methods
    -----------
    
    tokenize(text): list of tokens [(word,token)]
                    Return the list of words tokenized.
    
    >>> from monitorese.extractors.tweettokenizer import TweetTokenizer
    >>> tokenizer = TweetTokenizer()
    >>> tokenizer.tokenize('')
    []
    >>> tokenizer.tokenize("Empreendedores brazucas: menos eventos e oba-oba, mais testes. @dsheise no #MitA 017: http://bit.ly/kSkDe2")
    [('WORD', 'Empreendedores'), ('WORD', 'brazucas'), ('COLON', ':'), ('WORD', 'menos'), ('WORD', 'eventos'), ('WORD', 'e'), \
     ('WORD', 'oba-oba'), ('COMMA', ','), ('WORD', 'mais'), ('WORD', 'testes'), ('DOTS', '.'), ('@NAME', '@dsheise'), \
     ('WORD', 'no'), ('#TAG', '#MitA'), ('WORD', '017'), ('COLON', ':'), ('URL', 'http://bit.ly/kSkDe2')]
    '''
        
    def at_name(scanner,token):
        return '@NAME', token
    
    def colon(scanner,token):
        return 'COLON', token
    
    def url(scanner,token):
        return 'URL', token
    
    def hash_tag(scanner,token):
        return '#TAG', token
    
    def amp_quote(scanner, token):
        return '&QUOT', token
    
    def comma(scanner, token):
        return 'COMMA', token
    
    def question_mark(scanner,token):
        return 'QMARK' , token
    
    def emoticon(scanner, token):
        return 'EMOTICON', token
    
    def exclamation(scanner, token):
        return 'EXCLAIM', token
    
    def other(scanner, token):
        return 'OTHER', token
    
    def left_paren(scanner, token):
        return 'LEFT_PAREN', token
    
    def right_paren(scanner,token):
        return 'RIGHT_PAREN', token
    
    def dots(scanner,token):
        return 'DOTS', token
    
    def dashes(scanner, token):
        return 'DASHES' , token
    
    def percentage(scanner,token):
        return 'PERCENTAGE', token
    
    def dollar_amount(scanner,token):
        return 'DOLLARS', token
    
    def word(scanner,token):
        return 'WORD' , token
    
    def retweet(scanner,token):
        return 'RT', token
    
    def half_word(scanner, token):
        '''
            "Half" words are words at the end of tweets that 
            have been truncated due to the 140 character limit.
            These words usually end in 2 or more full stops.
        '''
        return "HALFWORD", token
    
    scanner = re.Scanner([ 
        ('&amp;', other),
        (r'/' , other),
        (r'\;-\)',emoticon),
        (r'\;', other),
        (r'\(', left_paren),
        (r'\)', right_paren),
        (r'\.+', dots),
        (r'\!', exclamation),
        (r':\(', emoticon),
        (r':\)', emoticon),
        (r':D', emoticon),
        (r'\,', comma),
        (r'\?', question_mark),
        (r'#[\w]+', hash_tag),
        (r'&quot;', amp_quote),
        (r'http://[^\s]+', url),
        (r'https://[^\s]+', url),
        (r'\:', colon),
        (r'@\w+', at_name),
        (r'\b-+\b', dashes),
        (r'\d+\%', percentage),
        (r'\$[0-9\.,]+', dollar_amount),
        (r'R\$[0-9\.,]+', dollar_amount),
        (r"[A-Za-z0-9'-/]+\.\.+", half_word),
        (r"\bRT\b", retweet),
        (r"\b[\w0-9'-/]+\b", word),
        (r"\s+", None),
        (r"[^\s]", other)
    ], re.U)
    
    @classmethod
    def tokenize(cls, text):
        tokens, remainder = cls.scanner.scan(text)
        if remainder:
            print "****input failed syntax*****"
            print "tokens:%s" % str(tokens)
            print "remainder:%s" % remainder
            raise TokenizerException
        return tokens

