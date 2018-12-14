from scrapy.http import Request
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
import csv
import datetime
import calendar
import scrapy
import time
import re
import MySQLdb
import datetime
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import logging
from pyvirtualdisplay import Display
import unicodedata
from ast import literal_eval


HEADERS =  {'pragma': 'no-cache',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'origin': 'https://hackforums.net',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'cache-control': 'no-cache',
            'authority': 'hackforums.net',
           }
class Hac_1(scrapy.Spider):
    name = 'hac_1'
    handle_httpstatus_list=[403]
    
    def start_requests(self):
	url = "https://hackforums.net/"
        time.sleep(3)
        yield Request(url, callback=self.parse, meta={'proxy':'http://74.70.67.218:59112'})

    def parse(self, response):
        sel = Selector(response)
        headers = {
        'authority': 'hackforums.net',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'origin': 'https://hackforums.net',
        'upgrade-insecure-requests': '1',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'https://hackforums.net/member.php?action=login',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        }
        data = {
        'username': 'kerspdr',
        'password': 'Inqspdr2018.',
        'quick_gauth_code': '',
        'submit': 'Login',
        'action': 'do_login',
        'url': 'https://hackforums.net/'
        }

        url_form = "https://hackforums.net/member.php"
        time.sleep(5)
        yield FormRequest(url_form, callback=self.parse_next, formdata=data, meta={'proxy':'http://74.70.67.218:59112'}, dont_filter=True)

    def parse_next(self, response):
        sel = Selector(response)
        import pdb;pdb.set_trace()


"""
        import pdb;pdb.set_trace()
        cookie = literal_eval(json.loads(json.dumps(
            str(response.headers)))).get('Set-Cookie', [])
        cookies = {}
        for i in cookie:
            data = i.split(';')[0]
            if data:
                try:
                    key, val = data.split('=', 1)
                except:
                    continue
                cookies.update({key.strip(): val.strip()})
	import pdb;pdb.set_trace()
        cookies_input = {
            'RFLovesYou_mybb[lastactive]': str(int(cookies.get('RFLovesYou_mybb[lastactive]', '')) + 283),
            'RFLovesYou_mybb[lastvisit]': cookies.get('RFLovesYou_mybb[lastvisit]', ''),
            'RFLovesYou_sid': cookies.get('RFLovesYou_sid', ''),
            '__cfduid': cookies.get('__cfduid', '')
	}
	url= 'https://hackforums.net/index.php'
"""
