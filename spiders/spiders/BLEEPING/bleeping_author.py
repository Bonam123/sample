import scrapy
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
import datetime
import time
import re
import MySQLdb
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import json
from datetime import date, timedelta
from bleeping_H_C import *

class BleepingSpider(scrapy.Spider):
    name = 'bleeping_author'

    def __init__(self):
        self.conn = MySQLdb.connect(db="BleepingComputer_DB", host="localhost", user="root", passwd="root", use_unicode=True, charset="utf8")
        self.cursor=self.conn.cursor()
        dispatcher.connect(self.close_conn, signals.spider_closed)

    def close_conn(self, spider):
        self.conn.commit()
        self.conn.close()

    def start_requests(self):
        yield FormRequest('https://www.bleepingcomputer.com/forums/index.php', callback=self.parse_next, headers=headers_a1, formdata=data_a1)

    def parse_next(self,response):
    
	st_que = 'select DISTINCT(links) from bleeping_crawl;'
	self.cursor.execute(st_que)
	data = self.cursor.fetchall()
        urls = []
        for da in data:
            urls.append(da[0])
        for url in urls:
            meta_query = 'select DISTINCT(auth_meta) from  bleeping_crawl where links = "%s"'%MySQLdb.escape_string(url.encode('utf8'))
            self.cursor.execute(meta_query)
            meta_query = self.cursor.fetchall()
            Publish_time = []
            threadtitle = []
            for da1 in meta_query:
                meta = json.loads(da1[0])
                threadtitle.append(meta.get('threadtitle',''))
                Publish_time.append(meta.get('Publish_time',''))
            Publish_time  = set (Publish_time)
            threadtitle = ', '.join(set(threadtitle))
            author_meta = {'Publish_time':Publish_time,'threadtitle':threadtitle}
	    if author_meta and url:
                yield FormRequest(url, callback=self.parse_author, headers=headers_a3, cookies=cookies_a3, meta = author_meta)

    def parse_author(self, response):
        threadtitle = response.meta.get('threadtitle','')
        sel = Selector(response)
    	username = ''.join(sel.xpath('//h1//span[@class="fn nickname"]//text()').extract())
        Domain = "www.bleepingcomputer.com"
        activetimes_ = response.meta.get('Publish_time')
    	activetimes = []
        try:
	        totalposts = int(''.join(response.xpath('//li[@class="clear clearfix"]//span[contains(text(),"Active Posts")]/../span[@class="row_data"]/text()').extract()).replace(',',''))
        except:
            totalposts = 0
            print 'vdnsjjj'
        for activetime in activetimes_:
            try:
                dt = time.gmtime(activetime/1000)
                activetime ="""[ { "year": "%s","month": "%s", "dayofweek": "%s", "hour": "%s", "count": "%s" }]"""%(str(dt.tm_year),str(dt.tm_mon),str(dt.tm_wday),str(dt.tm_hour),totalposts)
                activetimes.append(activetime)
            except:
                activetime = '-'
                activetimes.append(activetime)
        joindate = ''.join(response.xpath('//div[@id="user_info_cell"]/text()').extract())
        joindate = ''.join(re.findall('\w+, \d\d:\d\d \wM',joindate)) or ''.join(re.findall('\d\d \w+ \d\d\d\d',joindate))
        lastactive = ''.join(response.xpath('//span[contains(text(),"Last Active")]//text()').extract()).replace("Last Active ",'')
        try:
            joindate = datetime.datetime.strptime(joindate,'%d %b %Y')
            joindate = time.mktime(joindate.timetuple())*1000
        except:
            try:
                if 'esterday' in joindate:
                    joindate_ = date.today() - timedelta(1)
                    joindate_ = joindate_.strftime('%b %d %Y')+' '+''.join(re.findall('\d\d:\d\d \wM',joindate))
                    joindate = datetime.datetime.strptime(joindate_,'%b %d %Y %I:%M %p')
                    joindate = time.mktime(joindate.timetuple())*1000
                elif 'oday' in joindate:
                    joindate_ = date.today()
                    joindate_ = joindate_.strftime('%b %d %Y')+' '+''.join(re.findall('\d\d:\d\d \wM',joindate))
                    joindate = datetime.datetime.strptime(joindate_,'%b %d %Y %I:%M %p')
                    joindate = time.mktime(joindate.timetuple())*1000
            except:
                import pdb;pdb.set_trace()
        author_signature = ""
        try:
            lastactive = datetime.datetime.strptime(lastactive,'%b %d %Y %I:%M %p')
            lastactive =  time.mktime(lastactive.timetuple())*1000
        except:
            if 'esterday' in lastactive:
                yesterday = date.today() - timedelta(1)
                yesterday =  yesterday.strftime('%b %d %Y')+' '+''.join(re.findall('\d\d:\d\d \wM',lastactive))
                lastactive = datetime.datetime.strptime(yesterday,'%b %d %Y %I:%M %p')
                lastactive =  time.mktime(lastactive.timetuple())*1000
            elif 'oday' in lastactive:
                yesterday = date.today()
                yesterday = yesterday.strftime('%b %d %Y')+' '+''.join(re.findall('\d\d:\d\d \wM',lastactive))
                lastactive = datetime.datetime.strptime(yesterday,'%b %d %Y %I:%M %p')
                lastactive =  time.mktime(lastactive.timetuple())*1000
            else:
                lastactive = 00
        author_signature = ''.join(sel.xpath('//div[@class="signature"]/a//strong//text() | //div[@class="signature"]/a//following-sibling::text() | //div[@class="signature"]//span//text() | //div[@class="signature"]//text() | //div[@class="signature"]//p//img//@alt | //div[@class="signature"]//img//@alt').extract()).encode('utf-8')
        if not "smile.png" in author_signature:
            author_signature = ''.join(sel.xpath('//div[@class="signature"]/a//strong//text() | //div[@class="signature"]/a//following-sibling::text() | //div[@class="signature"]//span//text() | //div[@class="signature"]//text() | //div[@class="signature"]//p//img//@src').extract()).encode('utf-8')

        groups = ''.join(response.xpath('//li[@class="clear clearfix"]//span[contains(text(),"Group")]/..//span[@class="row_data"]//text()').extract())
        FetchTime = int(datetime.datetime.now().strftime("%s")) * 1000
        value = (MySQLdb.escape_string(threadtitle),username,Domain,'keepup',author_signature,joindate,\
                    lastactive,totalposts,FetchTime,groups,' ',' ',' ',' ',(''.join(activetimes)),' ',response.url,\
                    MySQLdb.escape_string(threadtitle), MySQLdb.escape_string(username),'keepup',joindate,lastactive,totalposts,FetchTime,groups,(''.join(activetimes)),response.url)
        query = 'INSERT INTO author(threadtitle,username,Domain,crawl_type,author_signature,join_date,lastactive,totalposts,FetchTime,groups,reputation,credits,awards,rank,activetime,contactinfo,reference_url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on DUPLICATE KEY UPDATE  threadtitle = %s, username = %s, crawl_type= %s, join_date= %s,lastactive= %s,totalposts= %s,FetchTime = %s,groups= %s,activetime= %s,reference_url= %s'
        self.cursor.execute(query,value)
