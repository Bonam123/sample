import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import re
import xlwt, xlrd
from scrapy.xlib.pydispatch import dispatcher
from openpyxl import Workbook
from scrapy import signals
import urllib
from scrapy.http import FormRequest

class Trade_India(scrapy.Spider):
    name = 'trade_india'
    start_urls = ['https://www.tradeindia.com/Seller/']

    row_count = 1 
    def __init__(self):
        self.empt_dict = {}
        self.file_ = xlwt.Workbook(encoding="utf-8")
        self.contain = self.file_.add_sheet("TRADE_INDIA")
	header = ['CATEGORY', 'LINK', 'TITLE','ADDRESS','PH_NUM']
        style = "font: bold on"
	self.row_count = 0
        for i, row in enumerate(header):
            self.contain.write(self.row_count, i, row, xlwt.Style.easyxf(style))
        dispatcher.connect(self.spider_closed, signals.spider_closed)
	self.row_count += 1

    def spider_closed(self):
        for key, value in self.empt_dict.iteritems():
            here_count = 0
            for eav in value:
	        self.contain.write(self.row_count, here_count, eav)
	        here_count += 1
	    self.row_count = self.row_count+1

   	self.file_.save("TRADE_INDIA.xlsx") 


    def parse(self, response):
        sel = Selector(response)
        category =['https://www.tradeindia.com/Seller/Apparel-Fashion/', 'https://www.tradeindia.com/Seller/Home-Supplies/', 'https://www.tradeindia.com/Seller/Health-Beauty/', 'https://www.tradeindia.com/Seller/Computer-Hardware-Software/', 'https://www.tradeindia.com/Seller/Consumer-Electronics/']
        #category =['https://www.tradeindia.com/Seller/Apparel-Fashion/']
        for cat in category:
            if "http" not in cat: cat = "https://www.tradeindia.com" + cat
            yield Request(cat, callback = self.parse_cat)

    def parse_cat(self, response):
        sel = Selector(response)
        sub_cate = sel.xpath('//a[contains(text(), "View More")]/@href').extract()
        for cat in sub_cate:
            if "http" not in cat: cat = "https://www.tradeindia.com" + cat
            yield Request(cat, callback = self.parse_add_cat)

    def parse_add_cat(self, response):
        sel = Selector(response)    
        add_sub_cate = sel.xpath('//a[contains(text(), "View More")]/@href').extract()
        if 'JavaScript:Void(0);' in add_sub_cate or not add_sub_cate:
            more_links = sel.xpath('//div[@class="divTableCell"]/a/@href').extract()
            for link in more_links:
                if "http" not in link: link = "https://www.tradeindia.com" + link
                yield Request(link, callback = self.parse_details)
        else:
            for cat in add_sub_cate:
                if "http" not in cat: cat = "https://www.tradeindia.com" + cat
                yield Request(cat, callback = self.parse_subcat)


    def parse_subcat(self, response):
        sel = Selector(response)
        more_links = sel.xpath('//div[@class="divTableCell"]/a/@href').extract()
        for link in more_links:
            if "http" not in link: link = "https://www.tradeindia.com" + link
            yield Request(link, callback = self.parse_details)
        if not more_links:
            url = response.url
            yield Request(url, callback = self.parse_details)


    def parse_details(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//div[@class="prod-info"]')
        for node in nodes:
            link = ''.join(node.xpath('.//span[@class="prod-title"]/a/@href').extract())
            title = ''.join(node.xpath('.//span[@class="prod-title"]//span//text()').extract()) or ''.join(node.xpath('.//a[@target="_blank"]//span//text()').extract())
            ph_num = ''.join(node.xpath('.//span[@class="mob"]//text()').extract())
            category = ''.join(re.findall('manufacturers/(.*).html',response.url))
	    if not ph_num:
		ph_num = ' '
            address = ''.join(node.xpath('.//span[@class="add-full tooltip-bottom bold"]//@data-tooltip').extract())
            self.empt_dict.update({address:[category, link, ph_num, address]})
            if "Bengaluru" in address:
                item = []
                item.append(category)
                item.append(link)
                item.append(title)
                item.append(address)
                item.append(ph_num)
        keywrd_id = ''.join(re.findall('manufacturers/(.*).html', response.url))
        cat_id = ''.join(sel.xpath('//input[@name="category_id"]/@value').extract())
        bus_id = ''.join(sel.xpath('//input[@name="business_kw_id"]/@value').extract())
        for i in range(1, 3): 
            page_id = str(i)
        headers = { 
            'pragma': 'no-cache',
            'cookie': '_ga=GA1.2.2029481776.1535182749; _gid=GA1.2.649993948.1535182749; privacy_policy=yes; __tawkuuid=e::tradeindia.com::HvTZ2pyvZeQr63J+SaZk/xzwd2LSlgvLa1d//YqVXcVVLOAZWUcdWJO6rIK6SFwm::2; Clickstream=a5152a67.5743d97a7bb78; TRADE_INDIA_SESSION_COOKIE=6ae5ea853ac928a9420f3179c1f41a81; AKA_A2=A; _gat_UA-99058809-1=1; TawkConnectionTime=0; RT="dm=tradeindia.com&si=9b18beb9-56fe-4033-a785-c3edf70c5bf4&ss=1535186837300&sl=41&tt=103039&obo=0&sh=1535190362237%3D41%3A0%3A103039%2C1535190296891%3D40%3A0%3A102017%2C1535189463283%3D39%3A0%3A99551%2C1535189448408%3D38%3A0%3A98496%2C1535189435832%3D37%3A0%3A97267&bcn=%2F%2F36fb61b5.akstat.io%2F&nu=&cl=1535190375192"',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,te;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            'accept': 'text/html, */*; q=0.01',
            'cache-control': 'no-cache',
            'authority': 'www.tradeindia.com',
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'https://www.tradeindia.com/',
        }

        params = ( 
            ('mode', 'product'),
            ('keyword', keywrd_id),
            ('cat_id', cat_id),
            ('business_kw_id', bus_id),
            ('show_other_components', '0'),
            ('page_no', '2'),
        )
        url = 'https://www.tradeindia.com/design2017/products/components/leaf_categories_product_listing_grid_list.html?'+urllib.urlencode(params)
        yield FormRequest(url, callback = self.parse_details)
        
