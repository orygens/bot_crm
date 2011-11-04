# -*- coding: utf-8 -*-
'''
Copyright (c) 2010 Monitore.se

bruno melo (bjmm@acm.org)
marcel@orygens.com
'''

import httplib
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup

def unshortenURL(link):
    try:
        o = urlparse.urlparse(link)
        conn = httplib.HTTPConnection(o.netloc)
        conn.request("GET", o.path) 
        r = conn.getresponse()
        realURL = r.getheader('Location')
        if realURL:
            return realURL.replace('&', '&amp;')
        else:
            return link
    except:
        return link

def __extract_url_title(link):
    try:
        req = urllib2.Request(link)
        response = urllib2.urlopen(req)
        soup = BeautifulSoup(response.read())
        return soup.title.string    
    except:
        return ""

def extract_url_info(link):
    '''
    >>> from monitorese.extractors.urlextractor import extract_url_info
    >>> extract_url_info('http://www.google.com')
    {'url': 'http://www.google.com.br/', 'title': u'Google'}
    '''
    
    unshorted = unshortenURL(link)
    return {'url': unshorted, 'title': __extract_url_title(unshorted)}
