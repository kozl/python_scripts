#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 19:02:50 2013

@author: z
"""
import os, os.path
import shelve
import json
import urllib2
import getpass
from urllib import urlencode, urlretrieve
from time import time
from vk_auth import vk_auth

from urlparse import urlsplit


CLIENT_ID = 3399430
SCOPE = ['friends','photos','groups','audio','docs','status','wall','messages','stats']
API_URL = 'https://api.vk.com/method/'

class VkAPI():
    def __init__(self, shelve_file='/tmp/at.db'):
        self.shelve_file = shelve_file
        self.access_token_db = shelve.open(self.shelve_file)
        os.chmod(self.shelve_file, 0600)
        try:            
            self.access_token = self.access_token_db['access_token']
            self.user_id = self.access_token_db['user_id']
            self.expires_in = self.access_token_db['expires_in']
            self.gen_time = self.access_token_db['gen_time']
            if not self.check_if_at_valid(): self.vk_auth()
        except KeyError: self.vk_auth()
        
    def check_if_at_valid(self):
        elapsed_time = int(self.expires_in) - (int(time()) - int(self.gen_time))
        if elapsed_time < 0: return False
        else: return True
    
    def vk_auth(self):
        self.email = raw_input('Enter email: ')
        self.password = getpass.getpass()
        self.access_token, self.user_id, self.expires_in, self.gen_time = vk_auth(self.email, self.password, CLIENT_ID, SCOPE)        
        
    def preserve_at(self):
        self.access_token_db['access_token'] = self.access_token
        self.access_token_db['user_id'] = self.user_id
        self.access_token_db['expires_in'] = self.expires_in
        self.access_token_db['gen_time'] = self.gen_time
        self.access_token_db.sync()
    
    def get(self, method, **params):
        params.update({"access_token" : self.access_token})
        conn = urllib2.urlopen(API_URL+"%s?%s" % (method, urlencode(params)))
        response = json.loads(conn.read())['response']
        return response

def download_photos(photo_list, path):
    for photo in photo_list:
        if 'src_xxxbig' in photo:
            url = photo['src_xxxbig']
        elif 'src_xxbig' in photo:
            url = photo['src_xxbig']
        elif 'src_xbig' in photo:
            url = photo['src_xbig']
        elif 'src_big' in photo:
            url = photo['src_big']
        filename = os.path.join(path, os.path.basename(urlsplit(url)[2]))
        urlretrieve(url, filename)