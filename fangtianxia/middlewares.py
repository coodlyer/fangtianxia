# -*- coding: utf-8 -*-
from __future__ import division
import requests, json, random
from scrapy import signals
from fangtianxia.user_agents import USER_AGENTS

class MyCustomDownloaderMiddleware(object):

    def __init__(self):
        self.ua = USER_AGENTS
    
    def process_request(self, request, spider):
        ua = random.choice(self.ua)
        request.headers.setdefault('User-Agent', ua)