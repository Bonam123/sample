import MySQLdb
import calendar
import time

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from exetools_xpaths import *
import datetime
import calendar
import csv
import re
import unicodedata

def clean_spchar_in_text(self, Text):
    '''
    Cleans up special chars in input text.
    input = "Hi!\r\n\t\t\t\r\n\t\t\t\r\n\t\t\t\r\n\t\t\r\n\r\n\t\t\r\n\t\t\r\n\t\t\t\r\n\t\t\tHi, besides my account"
    output = "Hi!\nHi, besides my account"
    '''
    #text = unicodedata.normalize("NFKD", Text)
    text = unicodedata.normalize('NFKD', Text.decode('utf8')).encode('utf8')
    text = re.compile(r'([\n,\t,\r]*\t)').sub('\n', Text)
    Text = re.sub(r'(\n\s*)', '\n', Text).encode('utf-8').encode('ascii', 'ignore')
    return Text


class Exetool(BaseSpider):
    name = "exetool"
    start_urls = urls

    def __init__(self):
        self.conn = MySQLdb.connect(db="EXETOOLS_DB", host="localhost",
                                    user="root", passwd="root", use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()


    def parse(self, response):
        thread_url = response.url.split('&')[0]
        domain = 'forum.exetools.com'
        if '&page=' in response.url:
            crawl_type = 'catchup'
        else:
            crawl_type = 'keepup'
        thread_title = ''.join(response.xpath(thread_title_xpath).extract()).strip()
        thread_topic = ''.join(response.xpath(thread_topic_xpath).extract()).strip()
        category = ''.join(thread_topic.split('> ')[1])
        sub_category = '["' + ''.join(thread_topic.split('> ')[2:]) + '"]'
        all_posts = response.xpath(all_posts_xpath).extract()
        for post in all_posts:
            Link = []
            sel = Selector(text=post)
            posted_url = ''.join(sel.xpath(posted_url_xpath).extract()).strip()
            post_ur = site_domain + posted_url
            post_url = ''.join(re.sub('s=(.*?)&', '',post_ur))
            if posted_url == '':
                continue
            try:
                post_id = post_url.split('&')[-2].split('=')[-1].strip()
            except:
                pass
            posted_time = ''.join(sel.xpath(posted_time_xpath).extract()).replace('\n', '').replace('\t', '').replace('\r', '').strip()
            publish_epoch = calendar.timegm(time.strptime(
                posted_time, '%m-%d-%Y, %H:%M')) * 1000
            fetch_time = calendar.timegm(time.gmtime()) * 1000
            ref_url = ''.join(sel.xpath(ref_url_xpath).extract())
            refe_url  = re.sub('s=(.*?)&', '', ''.join(sel.xpath(ref_url_xpath).extract()))
            if "http" not in refe_url: reference_url = site_domain + refe_url
            if not refe_url: reference_url = ""
            join_date = ''
            joindate = ''.join(sel.xpath(join_date_xpath).extract())
            if joindate:
                join_dt = joindate.replace('Join Date:','')
                join_date = time.mktime(time.strptime(join_dt,' %b %Y'))
            author = ''.join(
                sel.xpath('//a[@class="bigusername"]//text()').extract()).strip()

            author_url = site_domain + \
                ''.join(
                    sel.xpath('//a[@class="bigusername"]//@href').extract()).strip()
            author_url = ''.join(re.sub('s=(.*?)&', '',author_url))
            if author == '':
                auth_xp = '//td[@nowrap="nowrap"]//div[@id="%s"]//text()'
                title_id = 'postmenu_%s' % post_id
                auth_xp = auth_xp % title_id
                author = ''.join(sel.xpath('%s' % auth_xp).extract()).strip()
                author_url = ''
            if not author_url:
                author_url = ""

            comment_id = 'td_post_%s' % post_id
            post_xpath = comment_xpath % (comment_id, comment_id)
            Text_1 = ''.join(sel.xpath('//tr//td[contains(@id, "td_post")]//text() | //img//@title | //tr//td[contains(@id, "td_post")]//div[@class="smallfont"]//@alt | //a[@rel="nofollow"]//img[@class="inlineimg"]/@alt').extract()).strip().encode('utf8')
            author_signature = ''.join(sel.xpath(auth_sig_xpath).extract()).strip().encode('utf8')
            import pdb;pdb.set_trace()
            junk  = ''.join(sel.xpath('//tr//td[contains(@id, "td_post_")]//div[contains(@id, "post_message_")]/following-sibling::div//em//text()').extract()).strip().encode('utf8')
            if junk: author_signature = ""
            if "Last edited by chessgod101" in junk: author_signature = ''.join(sel.xpath(auth_sig_xpath).extract()).strip().encode('utf8')
            Text = Text_1.replace(author_signature,'')

            regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),~]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            text_links = re.findall(regex, Text)
            Link.extend(text_links)

            Text = clean_spchar_in_text(self, Text)

            link_xp = links_xpath % (comment_id, post_id)
            links = ','.join(sel.xpath('%s' % link_xp).extract()).strip()
            if author_signature: author_signature = ''.join(sel.xpath(auth_sig_xpath).extract()).strip().replace('_','').encode('utf8')
            if links != '':
                linkss = links.split(',')
                for link in linkss:
                    link = ''.join(re.sub('s=(.*?)&', '',link))
                    if ('.com' not in link) and ('http:' not in link) and ('https:' not in link):
                        new_link = site_domain + link
                        Link.append(new_link)
                        all_links = str(Link)
                    else:
                        Link.append(link)
                        all_links = str(Link)
            else:
                all_links = links
                all_links = list(set(all_links))
                all_links = ', '.join(all_links)
                if not all_links:
                        all_links = ""
            reputation = ''.join(sel.xpath(reputation_xpath).extract()).strip()
            reput = str(reputation.split('Rept. Rcvd ')[-1])
            repo = ''.join(re.findall('(\d+) Times', reput))
            groups_xp = group_xp_xpath % post_id
            group_obt = str(
                ''.join(sel.xpath(groups_xp).extract()).encode('utf8').strip())
            activetime = []
            totalposts = ''.join(sel.xpath(posts_xpath).extract()).strip().replace('Posts:','')
            if not totalposts: totalposts = ""
            activetimea = ''.join(sel.xpath(activetime_xpath).extract()).strip()
            lastactive = time.mktime(time.strptime(activetimea,'%m-%d-%Y, %H:%M'))
            try:
                dt= time.gmtime(int(time.mktime(time.strptime(activetimea,'%m-%d-%Y, %H:%M')))/1)
                activetime_ = """[ { "year": "%s","month": "%s", "dayofweek": "%s", "hour": "%s", "count": "%s" }]"""%(str(dt.tm_year),str(dt.tm_mon),str(dt.tm_mday),str(dt.tm_hour),totalposts)
                activetime.append(activetime_)
            except:
                activetime_ = ' '
                activetime.append(activetime_)
            activetime = ',  '.join(activetime)
            FetchTime = int(datetime.datetime.now().strftime("%s")) * 1000
            values = (domain,crawl_type,category, sub_category, MySQLdb.escape_string(thread_title), thread_url, post_id, post_url, publish_epoch, fetch_time, author.encode('utf-8'),author_url, Text.decode('utf8'), all_links, response.url, domain,crawl_type,category,sub_category,MySQLdb.escape_string(thread_title), thread_url, post_id, post_url, publish_epoch,fetch_time, author.encode('utf-8'),author_url,Text.decode('utf8'), all_links, response.url )

            query = 'insert ignore into exe_posts(domain,crawl_type,category,sub_category, thread_title, thread_url,\
                    post_id, post_url,publish_epoch, fetch_time, author,author_url,Text, all_links, reference_url)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE domain = %s, crawl_type= %s , category = %s, sub_category = %s ,thread_title = %s , thread_url = %s ,post_id = %s, post_url = %s,  publish_epoch = %s , fetch_time=%s,author = %s, author_url = %s,Text = %s, all_links = %s,reference_url = %s'

            self.cursor.execute(query, values)


            que = 'insert into exe_authors(username, Domain, crawl_type, author_signature, join_date, lastactive, totalposts, FetchTime, groups, reputation, credits, awards,rank, activetime, contactinfo, reference_url ) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE username = %s,Domain = %s, crawl_type= %s, author_signature = %s,join_date=%s, lastactive = %s, totalposts = %s, FetchTime=%s,groups = %s, reputation=%s,credits = %s, awards=%s,rank=%s,activetime =%s,contactinfo=%s,reference_url=%s'
            value = (author.encode('utf-8'), domain, crawl_type, author_signature, join_date,lastactive, totalposts, FetchTime, group_obt, repo, "", "","", activetime, "", reference_url, author.encode('utf-8'), domain, crawl_type, author_signature, join_date, lastactive, totalposts, FetchTime, group_obt, repo, "","","", activetime, "", reference_url )


            self.cursor.execute(que, value)

        next_page = set(response.xpath(next_page_xpath).extract())
        if next_page:
            new_link = list(next_page)
            next_page_url = site_domain + new_link[0]
            yield Request(next_page_url, self.parse)
