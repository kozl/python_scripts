#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 22:52:26 2013

@author: z
"""

import urllib2
import urlparse
import os.path
import os
import shelve
import time
from urllib import urlencode
import cookielib
from HTMLParser import HTMLParser


class VkFormParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.url = None
        self.params = {}
        self.in_form = False
        self.form_parsed = False
        self.method = "GET"
        
    def handle_starttag(self, tag, attrs):
        attrs = dict((name.lower(), value) for name, value in attrs)        
        if tag == "form":
            if self.form_parsed:
                raise RuntimeError("Second form on page")
            if self.in_form:
                raise RuntimeError("Already in form")
            self.in_form = True
            self.url = attrs["action"] 
            if "method" in attrs:
                self.method = attrs["method"]
        elif self.in_form and tag == "input" and "type" in attrs and "name" in attrs:
            if attrs["type"] in ["hidden", "text", "password"]:
                self.params[attrs["name"]] = attrs["value"] if "value" in attrs else ""
            
def handle_endtag(self, tag):
    tag = tag.lower()
    if tag == "form":
        if not self.in_form:
            raise RuntimeError("Unexpected end of <form>")
        self.in_form = False
        self.form_parsed = True

def vk_auth(email, password, client_id, scope):    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
                              urllib2.HTTPRedirectHandler)
                              
    response = opener.open("http://oauth.vk.com/oauth/authorize?" + \
                       "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
                       "client_id=%s&scope=%s&display=wap" % (client_id, ','.join(scope)))
    parser=VkFormParser()
    parser.feed(response.read())
    parser.params["email"] = email
    parser.params["pass"] = password
    response = opener.open(parser.url,urlencode(parser.params))    
    if not 'blank.html' in urlparse.urlparse(response.geturl())[2]:
        parser = VkFormParser()
        parser.feed(response.read())
        response = opener.open(parser.url,urlencode(parser.params))
    curr_time = time.time()
    resp_params = urlparse.parse_qs(urlparse.urlparse(response.geturl())[5])
    return (resp_params['access_token'][0], resp_params['user_id'][0], resp_params['expires_in'][0], curr_time)