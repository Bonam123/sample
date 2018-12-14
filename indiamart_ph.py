# uncompyle6 version 3.2.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Dec  4 2017, 14:50:18) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/amrutha/yellow/yellow/spiders/indiamart_ph.py
# Compiled at: 2018-10-02 16:14:14
import scrapy, requests
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
import re, urllib, json, xlwt, xlrd
from scrapy.xlib.pydispatch import dispatcher
from openpyxl import Workbook
from scrapy import signals

class Indiamart_ph(scrapy.Spider):
    name = 'indiamart_ph'
    start_urls = ['https://dir.indiamart.com/bengaluru/mobile-phones.html']
    row_count = 1

    def __init__(self):
        self.file_ = xlwt.Workbook(encoding='utf-8')
        self.contain = self.file_.add_sheet('INDIA_MART')
        header = ['PROD_TITLE', 'PROD_ADD_TITLE', 'PROD_ADDRESS', 'PH_NUM', 'CONTACT_PERSON']
        style = 'font: bold on'
        for i, row in enumerate(header):
            self.contain.write(0, i, row, xlwt.Style.easyxf(style))

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.file_.save('INDIA_MART.xlsx')

    def parse(self, response):
        sel = Selector(response)
        gh = ('').join(sel.xpath('//div[@id="page_variables"]//script[@type="text/javascript"]//text()').extract())
        mac_id = ('').join(re.findall('mcatID:(.*)}}', gh))
        mac_id = mac_id.replace('"', '') or ('').join(re.findall('mcatId=(\\d+)', response.url))
        mac_name = ('').join(re.findall('bengaluru/(.*).html', response.url)) or ('').join(re.findall('&mcatName=(\\D+)&', response.url))
        if '/impcat/next' in response.url:
            url_ = response.meta.get('url_', '')
        else:
            url_ = response.url
        city_ = ('').join(sel.xpath('//div[@class="disp-none blG-st0"]//following-sibling::script[@type="text/javascript"]//text()').extract())
        city_id = ('').join(re.findall('ims.cityID = (.*); ims.time', city_))
        city_id = city_id.replace("'", '')
        city_id = ('').join(re.findall('(.*);', city_id)) or ('').join(re.findall('&cityID=(\\d+)', response.url))
        for i in range(2, 4):
            pg_id = str(i)

        start = 29
        end = ''
        nodes = sel.xpath('//li[contains(@class, "lst lst_cl")]')
        for node in nodes:
            prod_name = ('').join(node.select('.//span[contains(@class, "pnm ldf cur")]//text()').extract())
            prod_add_1 = ('').join(node.select('.//span/a[@class="lcname"]//text()').extract())
            ph_num = ('').join(node.select('.//span[@class="ls_co phn bo"]//span[contains(@id, "pns")]//following-sibling::text()').extract())
            prod_main_add = ('').join(node.select('.//div[@class="clg"]//text()').extract())

        for ia, st in enumerate(range(2)):
            if ia == 0:
                start = start
                end = start + 27
            else:
                start = end + 1
                end = start + 19

        headers = {'pragma': 'no-cache', 
           'accept-encoding': 'gzip, deflate, br', 
           'accept-language': 'en-US,en;q=0.9,te;q=0.8', 
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36', 
           'accept': '*/*', 
           'cache-control': 'no-cache', 
           'authority': 'dir.indiamart.com', 
           'x-requested-with': 'XMLHttpRequest', 
           'referer': url_}
        params = (
         (
          'mcatId', mac_id),
         (
          'mcatName', mac_name),
         (
          'srt', start),
         (
          'end', end),
         ('ims_flag', ''),
         (
          'cityID', city_id),
         ('cityNm', 'Bengaluru'),
         ('fcilp', '0'),
         ('pr', '0'),
         (
          'pg', pg_id))
        links = sel.xpath('//a[@class="pnm ldf cur"]/@href').extract()
        for link in links:
            yield Request(link, callback=self.parse_links)

        url = 'https://dir.indiamart.com/impcat/next?' + urllib.urlencode(params)
        yield Request(url, callback=self.parse, headers=headers, meta={'url_': url_, 'start': start, 'end': end, 'pg_id': pg_id})
        if '/impcat/nex' in response.url:
            data_ = json.loads(response.body)
            sel = Selector(text=data_['content'])
            mac_id = ('').join(re.findall('mcatId=(\\d+)', response.url))
            mac_name = ('').join(re.findall('&mcatName=(\\D+)&', response.url))
            if '/impcat/next' in response.url:
                url_ = response.meta.get('url_', '')
            else:
                url_ = response.url
            start = response.meta.get('start', '')
            end = response.meta.get('end', '')
            city_id = ('').join(re.findall('&cityID=(\\d+)', response.url))
            pg_id = response.meta.get('pg_id', '')
            pg_id = int(pg_id) + 1
            nodes = sel.xpath('//li[contains(@class, "lst lst_cl")]')
            for node in nodes:
                prod_name = ('').join(node.select('.//span[contains(@class, "pnm ldf cur")]//text()').extract())
                prod_add_1 = ('').join(node.select('.//span/a[@class="lcname"]//text()').extract())
                ph_num = ('').join(node.select('.//span[@class="ls_co phn bo"]//span[contains(@id, "pns")]//following-sibling::text()').extract())
                prod_main_add = ('').join(node.select('.//div[@class="clg"]//text()').extract())

            for ia, st in enumerate(range(2)):
                start = end + 1
                end = start + 19
                headers = {'pragma': 'no-cache', 
                   'accept-encoding': 'gzip, deflate, br', 
                   'accept-language': 'en-US,en;q=0.9,te;q=0.8', 
                   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36', 
                   'accept': '*/*', 
                   'cache-control': 'no-cache', 
                   'authority': 'dir.indiamart.com', 
                   'x-requested-with': 'XMLHttpRequest', 
                   'referer': url_}
                params = (
                 (
                  'mcatId', mac_id),
                 (
                  'mcatName', mac_name),
                 (
                  'srt', start),
                 (
                  'end', end),
                 ('ims_flag', ''),
                 (
                  'cityID', city_id),
                 ('cityNm', 'Bengaluru'),
                 ('fcilp', '0'),
                 ('pr', '0'),
                 (
                  'pg', pg_id))
                links = sel.xpath('//a/@href').extract()
                for link in links:
                    yield Request(link, callback=self.parse_links)

                url = 'https://dir.indiamart.com/impcat/next?' + urllib.urlencode(params)
                yield Request(url, callback=self.parse, headers=headers, meta={'url_': url_, 'start': start, 'end': end, 'pg_id': pg_id})

    def parse_links(self, response):
        sel = Selector(response)
        prod_title = ('').join(sel.xpath('//h1[@class="bo"]//text()').extract())
        if not prod_title:
            prod_title = response.url
        prod_add_title = ('').join(sel.xpath('//div[@class="fs15"]//text()').extract()) or ('').join(sel.xpath('//span[@class="com-name ds bo2"]//text()').extract())
        prod_add_title = prod_add_title.strip()
        prod_address = ('').join(sel.xpath('//span[@class="color1 dcell verT fs13"]//text()').extract()) or ('').join(sel.xpath('//p[@class="contact-nam fl m33"]//text()').extract())
        prod_address = prod_address.strip()
        ph_num = ('').join(sel.xpath('//span[@id="pns_no2"]//text()').extract()) or ('').join(sel.xpath('//span[@id="footer_pns"]/text()').extract())
        if not ph_num:
            ph_num = ' '
        cont_person = ('').join(sel.xpath('//div[@id="supp_nm"]//text()').extract()) or ('').join(sel.xpath('//span[@class="fnt8_sh clr9 bo2"]//text()').extract())
        item = []
        item.append(prod_title)
        item.append(prod_add_title)
        item.append(prod_address)
        item.append(ph_num)
        item.append(cont_person)
        for col_count, value in enumerate(item):
            self.contain.write(self.row_count, col_count, value)

        self.row_count = self.row_count + 1
        print self.row_count
        import pdb;pdb.set_trace()
        if self.row_count >= 20:
            import pdb;pdb.set_trace()
