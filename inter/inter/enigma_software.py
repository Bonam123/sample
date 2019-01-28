import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
import re
import MySQLdb
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class Enigma_Software(scrapy.Spider):
    name = "enigma_software"
    start_urls = ['https://www.enigmasoftware.es/threat-database/']

    def __init__(self,*args, **kwargs):
        super(Enigma_Software, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(db="ENIGMA_DB", host="localhost",user="root",passwd="root",use_unicode=True,charset="utf8")
        self.cursor=self.conn.cursor()
        dispatcher.connect(self.close_conn, signals.spider_closed)

    def close_conn(self, spider):
        self.conn.commit()
        self.conn.close()


    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//table[@class="top_table"]//td[@style]/a/@href').extract()
        for link in links:
            link = "https://www.enigmasoftware.com/threat-database/rogue-anti-virus-program/2/"
            yield Request(link, callback=self.parse_threads)

    def parse_threads(self, response):
        sel = Selector(response)
        cat_title = ''.join(sel.xpath('//h1[@class="title"]//text()').extract()).replace('\n','').replace('\t','')
        nodes = sel.xpath('//table[@class="top_table"]//tr')
        for node in nodes:
            import pdb;pdb.set_trace()
            headers = ''.join(node.xpath('.//text()').extract())
            if "name" in headers.lower() or "date"  in headers.lower(): continue
            title = ''.join(node.xpath('.//td/a[@style]//text()').extract()).replace('\n','').replace('\t','')
            url = ''.join(node.xpath('.//td/a[@style]//@href').extract()).replace('\n','').replace('\t','')
            if "http" not in url: 
                url = "https://www.enigmasoftware.com" + url
            detection_count = ''.join(node.xpath('.//td[@style]//text()').extract()).replace('\n','').replace('\t','')
            date_ = ''.join(node.xpath('.//td[@class="priority-low"]//text()').extract()).replace('\n','').replace('\t','')
            threat_level = ''.join(node.xpath('.//td//span//text()').extract()).replace('\n','').replace('\t','')
            threat_level_count = ''.join(re.findall('(.*)/',threat_level))
            t_val = (cat_title, url, title, detection_count, threat_level_count, date_, response.url)
            '''query = "INSERT INTO thread_data(cat_title, url,  title, detection_count, threat_level_count, date_)\
                    VALUES('%s','%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE cat_title = %s, url = %s, \
                    title = %s, detection_count = %s, threat_level_count = %s, date_ = %s"'''
            query="INSERT INTO thread_data(cat_title, url,  title, detection_count, threat_level_count, date_,reference_url)VALUES(%s,%s,%s,%s,%s,%s,%s)"
            #self.cursor.execute(t_val, query)
            self.cursor.execute(query,t_val)

        nxt_pg = ''.join(sel.xpath('//a[contains(text(), "Next")]/@href').extract())
        if nxt_pg:
            if "http" not in nxt_pg: nxt_pg =   "https://www.enigmasoftware.com" + nxt_pg
            print nxt_pg
            yield Request(nxt_pg, callback=self.parse_threads)



            
