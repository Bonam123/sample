import scrapy
from scrapy. selector import Selector
from scrapy.http import Request
import json, re

class Aus_remo(scrapy.Spider):
    name = "aus_remo"
    start_urls = ['https://aus.remonews.com/']

    def parse(self, response):
        sel = Selector(response)
        cate = sel.xpath('//li[contains(@id, "menu-item")]/a/@href').extract()
        for cat in cate:
            yield Request(cat, callback = self.parse_links)

    def parse_links(self, response):
        sel = Selector(response)
        links = sel.xpath('//article[@class="item-list"]//h2[@class="post-box-title"]/a/@href').extract()
        for link in links:
            yield Request(link, callback = self.parse_details)

        nxt_pg = ''.join(sel.xpath('//span[@id="tie-next-page"]/a/@href').extract())
        if nxt_pg:
            yield Request(nxt_pg, callback = self.parse_links)

    def parse_details(self, response):
        sel = Selector(response)
        title = ''.join(sel.xpath('//h1[@class="name post-title entry-title"]//span//text()').extract())
        text = ''.join(sel.xpath('//div[@class="entry"]//p//text()').extract())
        text = text.replace("\n\r\n\r\n\r\n\r\n(adsbygoogle = window.adsbygoogle || []).push({});\r\n\n",'')
        date_scr =  ''.join(sel.xpath('//script[@type="application/ld+json"]//text()').extract())
        date_ =  json.loads(date_scr)
        dat =  date_.get('datePublished', {})
        dt = ''.join(re.findall('(.*)T', dat))
        if title == '' or text == ''  or date_ == '':
            import pdb;pdb.set_trace()
    
