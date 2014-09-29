#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Sat Mar 30 13:43:16 2013

@author: z
"""

import HTMLParser
import urllib2
from urllib import urlencode
import cookielib
import cgi
import sys
import re

URL_LOGIN = 'https://www.numberingplans.com/?page=account&sub=login'
URL_PHONE = 'http://www.numberingplans.com/?page=analysis&sub=phonenr'
URL_IMEI = 'http://www.numberingplans.com/?page=analysis&sub=imeinr'
URL_IMSI = 'http://www.numberingplans.com/?page=analysis&sub=imsinr'
URL_SIMNR = 'http://www.numberingplans.com/?page=analysis&sub=simnr' 


def parse_np_page(text):
    res = re.search(r'<table.*>.*</table>', text, re.DOTALL)
    return res.group()

def print_html_for_cgi(text):
    print "Content-Type: text/html"
    print
    print '''
<HTML>
  <BODY>
    %s
  </BODY>	
<HTML>
''' % text

if __name__ == '__main__':
    form = cgi.FieldStorage()    
    cookie_handler   = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    redirect_handler = urllib2.HTTPRedirectHandler()
    http_handler     = urllib2.HTTPHandler()
    https_handler    = urllib2.HTTPSHandler()
    opener = urllib2.build_opener(http_handler,
                                  https_handler,
                                  redirect_handler,
                                  cookie_handler)
    user_agent='Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'
    opener.addheaders = [('User-agent', user_agent)]
    opener.open(URL_LOGIN, urlencode(dict(username='***',
                                                password='***'))) 
    res = opener.open(URL_PHONE, urlencode(dict(i=form['i'])))
    table =  parse_np_page(res.read())
    print_html_for_cgi(table)
