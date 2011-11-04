"""

Copyright (c) 2010 Monitore.se
marcel@orygens.com

This module is the placeholder for helper classes and functions for the extractors.

"""

import datetime

class TokenizerException(Exception):
	pass
	
	
def fix_date_format(date_string):
    return datetime.datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S +0000") - datetime.timedelta(hours=3)