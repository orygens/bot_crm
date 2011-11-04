#-*- coding:utf-8 -*-
"""

Copyright (c) 2010 Monitore.se
marcel@orygens.com

"""

import re
import sys
from utils import TokenizerException
  

class BasicTokenizer(object):
	'''
	This class is the basic Tokenizer, which is responsable of:
	 1. Ignores most punctuation and simply returns the words.

	Tokenizer for News/Blog headlines that ignores most punctuation and simply 
	returns the words.

	The tokens can then be further processed with the Keyword Tagger for example.
	
	Parameters
	-----------
	text : string  Text that will be tokenized.
	
	Methods
	-----------
	
	tokenize(text): list of tokens [(word,token)]
	                Return the list of words tokenized.
	
	>>> from monitorese.extractors.basictokenizer import BasicTokenizer
	>>> tokenizer = BasicTokenizer()
	>>> tokenizer.tokenize('')
	[]
	>>> tokenizer.tokenize("Empreendedores brazucas: menos eventos e oba-oba, mais testes. @dsheise no #MitA 017: http://bit.ly/kSkDe2")
	['Empreendedores', 'brazucas', 'menos', 'eventos', 'e', 'oba', 'oba', 'mais', 'testes', 'dsheise', 'no', 'MitA', '017', 'http', 'bit', 'ly', 'kSkDe2']
	'''
	
	def word(scanner,token):
		return 'WORD' , token
	
	scanner = re.Scanner([ 
		(r'\W+', None),
		(r'\b\w+\b',word)
	])
	
	
	@classmethod
	def tokenize(cls,text):
		tokens, remainder = cls.scanner.scan(text)
		if remainder:
			print '***input failed syntax***'
			print 'tokens:%s' % str(tokens)
			print 'remainder: %s' % remainder
			raise TokenizerException
		include = ('WORD',)
		tokens = [ t[1] for t in tokens if t[0] in include]
		return tokens