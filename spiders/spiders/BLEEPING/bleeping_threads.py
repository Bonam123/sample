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
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 
from bleeping_H_C import *
import unicodedata


def clean_spchar_in_text(self, text):
    ''' 
    Cleans up special chars in input text.
    input = "Hi!\r\n\t\t\t\r\n\t\t\t\r\n\t\t\t\r\n\t\t\r\n\r\n\t\t\r\n\t\t\r\n\t\t\t\r\n\t\t\tHi, besides my account"
    output = "Hi!\nHi, besides my account"
    '''
    #text = unicodedata.normalize("NFKD", Text)
    text = unicodedata.normalize('NFKD', text.decode('utf8')).encode('utf8')
    text = re.compile(r'([\n,\t,\r]*\t)').sub('\n', text)
    text = re.sub(r'(\n\s*)', '\n', text).encode('utf-8').encode('ascii', 'ignore')
    return text



class BleepingSpider(scrapy.Spider):
    name = 'bleeping_threads'

    def __init__(self):
        self.conn = MySQLdb.connect(db="BleepingComputer_DB", host="localhost", user="root", passwd= "root",use_unicode=True, charset="utf8")
        self.cursor=self.conn.cursor()  
        dispatcher.connect(self.close_conn, signals.spider_closed)

    def close_conn(self, spider):
        self.conn.commit()
        self.conn.close()

    def start_requests(self):
        yield FormRequest('https://www.bleepingcomputer.com/forums/index.php', callback=self.parse_1st,headers=headers_1,formdata=data_1)

    def parse_1st(self,response):
        sel = Selector(response)
        urls = sel.xpath(urls_xpath).extract()
        for url in urls:
            if "https://www.bleepingcomputer.com/" in url:
                yield FormRequest(url,callback = self.parse_next, headers=headers_2, cookies=cookies_2)
            
    def parse_next(self,response):
        sel = Selector(response)
        thread_urls = response.xpath(thread_urls_xpath).extract()
        for url in thread_urls:
            if "bleepingcomputer" in url:
                #url = "https://www.bleepingcomputer.com/forums/t/678874/bios-update-caused-booting-freeze-when-3tb-drives-are-connected/#entry4510827"
                url = "https://www.bleepingcomputer.com/forums/t/682819/email-outlook-cant-send-or-receive/#entry4585240"
                yield FormRequest(url, callback=self.parse_threads, headers=headers_3, cookies=cookies_3)	

        navigation = ''.join(response.xpath(navigation_xpath).extract())
        if navigation:
            print navigation
            yield Request(navigation, callback = self.parse_next, headers=headers_2, cookies=cookies_2)


    def parse_threads(self,response):
        ThreadUrl = response.url
        if '/page-' in response.url:
            crawl_type = 'catch up'
            test = re.findall('page-\d+',response.url)
            ThreadUrl = response.url.replace(''.join(test),"")
        else:
            crawl_type = 'keep up'
            ThreadUrl = response.url
        sel = Selector(response)
        Domain = "www.bleepingcomputer.com"
        Category = sel.xpath(Category_xpath).extract()[1]
        Subcategory = str([sel.xpath(Subcategory_xpath).extract()[-1].encode('utf8')])
        ThreadTitle = ''.join(sel.xpath(ThreadTitle_xpath).extract()).replace('\\','').strip()
        nodes = sel.xpath(nodes_xpath)
        link = ''
        for node in nodes:
            text = ""
            text = ''.join(node.xpath('.//div[@class="post entry-content "]//text()').extract())
            if "http" not in text:
                text = ''.join(node.xpath('.//div[@class="post entry-content "]//text() | .//div[@class="post entry-content "]//span[@rel="lightbox"]//@alt | .//iframe[@class="EmbeddedVideo"]//@alt | .//img[@class="attach"]//@src | .//div[@class="post entry-content "]//a[@class="bbc_url"]/@href | .//div[@class="post entry-content "]//li[@class="attachment"]//a[img]/@href | .//div[@class="post entry-content "]//li[@class="attachment"]//a[strong]//text() | .//div[@class="post entry-content "]//p//img/@alt | .//div[@class="post entry-content "]//img/@alt').extract())
            if ".jpg" in text:
                text = ''.join(node.xpath('.//div[@class="post entry-content "]//text() | .//div[@class="post entry-content "]//span[@rel="lightbox"]//@src | .//iframe[@class="EmbeddedVideo"]//@alt | .//img[@class="attach"]//@src | .//div[@class="post entry-content "]//a[@class="bbc_url"]/@href | .//div[@class="post entry-content "]//li[@class="attachment"]//a[img]/@href | .//div[@class="post entry-content "]//li[@class="attachment"]//a[strong]//text() | .//div[@class="post entry-content "]//p//img/@alt').extract())
            junk=  ''.join(node.xpath('.//div[@class="post entry-content "]//p[@style="text-align:center"]//a//img[@class="bbc_img"]/@alt').extract())
            text = text.replace(junk,'')
            link = ''.join(node.xpath('.//div[@id="gifv"]//video/source/@src').extract())
            if link :
                if ('.com' not in link) or  ('http:' not in link) or ('https:' not in link): link = "http" + link
            text = text + link
            auth_= dt_ = date_ = ""
            auth_ = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author').extract())
            dt_ = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-date').extract())
            if auth_ and dt_:
                text = ''.join(node.xpath('.//div[@class="post entry-content "]//text() | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-date | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author | .//div[@class="post entry-content "]//span[@rel="lightbox"]//@src | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time | .//div[@class="post entry-content "]//p//img/@alt').extract())
                dt_said = dt_ + ", said: "
                auth_on = "Quote " + auth_ + ", on "
                text = text.replace(auth_, auth_on).replace(dt_, dt_said)
            if auth_ and dt_ and len(auth_) >15:
                auth_ = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author').extract())
                date_ = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time').extract())
                text = ''.join(node.xpath('.//div[@class="post entry-content "]//text() | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-date | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author | .//div[@class="post entry-content "]//span[@rel="lightbox"]//@src | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time | .//div[@class="post entry-content "]//p//img/@alt').extract())
                auth_1 = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author').extract()[0])
                auth_2 = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author').extract()[1])
                date_1 = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time').extract()[0])
                date_2 = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time').extract()[1])
                auth_on_1 = "Quote " + auth_1 + ", on "
                auth_on_2 = "Quote " + auth_2 + ", on "
                acd_1 = int(date_1)
                acd_2 = int(date_2)
                asd_1 = time.strftime('%d %b %Y - %I:%M %p', time.localtime(acd_1))
                asd_2 = time.strftime('%d %b %Y - %I:%M %p', time.localtime(acd_2))
                dt_said_1 = asd_1 + ", said: "
                dt_said_2 = asd_2 + ", said: "
                text = text.replace(auth_1, auth_on_1).replace(date_1, dt_said_1).replace(auth_2,auth_on_2).replace(date_2, dt_said_2)
            if not dt_:
                auth_ = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author').extract())
                date_ = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time').extract())
            if date_ and auth_:
                text = ''.join(node.xpath('.//div[@class="post entry-content "]//text() | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-date | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author | .//div[@class="post entry-content "]//span[@rel="lightbox"]//@src | .//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time | .//div[@class="post entry-content "]//p//img/@alt').extract())
                try:
                    acd = int(date_)
                    asd = time.strftime('%d %b %Y - %I:%M %p', time.localtime(acd))
                    dt_said = asd + ", said: "
                    auth_on = "Quote " + auth_ + ", on "
                    text = text.replace(auth_, auth_on).replace(date_, dt_said)
                except:
                    pass
                if len(auth_) > 15:
                    auth_1 = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author').extract()[0])
                    auth_2 = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-author').extract()[1])
                    date_1 = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time').extract()[0])
                    date_2 = ''.join(node.xpath('.//div[@itemprop="commentText"]//following-sibling::blockquote//@data-time').extract()[1])
                    auth_on_1 = "Quote " + auth_1 + ", on "
                    auth_on_2 = "Quote " + auth_2 + ", on "
                    acd_1 = int(date_1)
                    acd_2 = int(date_2)
                    asd_1 = time.strftime('%d %b %Y - %I:%M %p', time.localtime(acd_1))
                    asd_2 = time.strftime('%d %b %Y - %I:%M %p', time.localtime(acd_2))
                    dt_said_1 = asd_1 + ", said: "
                    dt_said_2 = asd_2 + ", said: "
                    text = text.replace(auth_1, auth_on_1).replace(date_1, dt_said_1).replace(auth_2,auth_on_2).replace(date_2, dt_said_2)
            text = text.replace('snapshot.png', '')
            text = clean_spchar_in_text(self,text)
            author_links = ''.join(node.xpath('.//span[@class="author vcard"]//a//@href').extract()).strip() 
            if  not author_links:pass
            Posturl =','.join(node.xpath(Post_url_xpath).extract()).strip()
            Postid = ''.join(re.findall('entry\d+',Posturl)).replace('entry','').strip()
            PublishTime = ''.join(node.xpath(PublishTime_xpath).extract()).strip()
            try:
                PublishTime = datetime.datetime.strptime(PublishTime, '%d %B %Y - %H:%M %p') 
                PublishTime = time.mktime(PublishTime.timetuple())*1000
            except:
                try:
                    if 'Yesterday' in PublishTime:
                        today = round(time.time()*1000) - 24*60*60*1000
                        am = ''.join(re.findall('\d+:\d+ AM',PublishTime))
                        pm = ''.join(re.findall('\d+:\d+ PM',PublishTime))
                        if am:
                            H = int(am[0:2])
                            M = int(am[3:5])
                        if pm:
                            H = int(pm[0:2])+12
                            M = int(pm[3:5])
                        dt = H*60*60*1000+ M*60*1000
                        PublishTime = today + dt
                except:
                    import pdb;pdb.set_trace()
            FetchTime = round(time.time()*1000)
            Link = []
            linkss = node.xpath(Links_xpath).extract()
            for link in linkss:
                Link.append(link)
            Links = str(Link)
            if "[]" in Links:
                Links = ""
            Author = ''.join(set(node.xpath(Author_xpath).extract())).strip()
            query = 'insert into Threads(Domain,Category,Subcategory,ThreadTitle,ThreadUrl,PostId,PostUrl,PublishTime,FetchTime,Author,Text,Links,reference_url,crawl_type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)ON DUPLICATE KEY UPDATE Category = %s, Subcategory = %s, ThreadTitle = %s, ThreadUrl = %s, PostId = %s,PostUrl = %s,PublishTime = %s,FetchTime = %s,Author = %s,Text = %s,Links = %s,reference_url = %s, crawl_type = %s '
            values = (Domain,Category,Subcategory,ThreadTitle,ThreadUrl,Postid,Posturl,\
                    PublishTime,FetchTime,Author,text.encode('utf8'),\
                    Links,response.url,crawl_type, Category,Subcategory,ThreadTitle,ThreadUrl,\
                    Postid,Posturl, PublishTime,FetchTime,Author,text.encode('utf8'),\
                    Links,response.url,crawl_type)
            self.cursor.execute(query,values)
            meta = json.dumps({'Publish_time':PublishTime,'threadtitle':ThreadTitle})
            que_to_auth = 'insert into bleeping_crawl(links, auth_meta, PostId)values("%s","%s","%s")ON DUPLICATE KEY UPDATE links = "%s", auth_meta = "%s"'%(MySQLdb.escape_string(author_links.encode('utf8')),MySQLdb.escape_string(meta),Postid,MySQLdb.escape_string(author_links.encode('utf8')),MySQLdb.escape_string(meta))
            self.cursor.execute(que_to_auth)
        
        nxt_pg = ''.join(sel.xpath('//link[@rel="stylesheet"]//following-sibling::link[@rel="next"]/@href').extract())
        if nxt_pg:
            yield Request(nxt_pg,callback = self.parse_threads,cookies=cookies_,headers=headers_)
