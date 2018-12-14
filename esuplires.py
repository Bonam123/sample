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


class Esuplires(scrapy.Spider):
    name = 'esuplires'
    #start_urls = ["http://www.esuppliersindia.com/products/computer-hardware-software/"]
    start_urls = ["http://www.esuppliersindia.com/products/consumer-electronics/"]

    row_count = 1 
    def __init__(self):
        self.empt_dict = {}
        self.file_ = xlwt.Workbook(encoding="utf-8")
        self.contain = self.file_.add_sheet("TRADE_INDIA")
        header = ['TITLE','ADDRESS','PH_NUM','CATEGORY','FAX','MOBILE','CONTACT_PERSON']
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

        self.file_.save("ESUPPLIERS.xlsx") 


    def parse(self, response):
        sel = Selector(response)
        cate = sel.xpath('//strong[@class="oragne-f12b"]/a/@href').extract()
        for cat in cate:
            if "http" not in cat: cat =  "http://www.esuppliersindia.com" + cat
            yield Request(cat, callback=self.parse_links)

    def parse_links(self, response):
        sel = Selector(response)
        links = sel.xpath('//td[@class="bl-undl-link"]/a/@href').extract()
        for link in links:
            if "http" not in link: link =   "http://www.esuppliersindia.com" + link
            yield Request(link, callback = self.parse_other_links)

        if not links:
            cates = sel.xpath('//strong[@class="oragne-f12b"]/a/@href').extract()
            for cate in cates:
                if "http" not in cate: cate =  "http://www.esuppliersindia.com" + cate
                yield Request(cate, callback = self.parse_links)
            if not cates:
                add_nodes =  sel.xpath('//td[@class="orangebg"]')
                for node in add_nodes:
                    linkw = ''.join(node.xpath('./a/@href').extract())
                    if "http" not in linkw: linkw =   "http://www.esuppliersindia.com" + linkw
                    category = ''.join(node.xpath('./a/text()').extract())
                    yield Request(linkw, callback = self.parse_details, meta={'category':category})

    def parse_other_links(self, response):
        sel = Selector(response)
        place = sel.xpath('//td[span[@class="blue-f11-b"]]/text()').extract()
        for place_ in place:
            if "Bengaluru" in place_:
                add_nodes =  sel.xpath('//td[@class="orangebg"]')
                for node in add_nodes:
                    linkw = ''.join(node.xpath('./a/@href').extract())
                    if "http" not in linkw: linkw =   "http://www.esuppliersindia.com" + linkw
                    category = ''.join(node.xpath('./a/text()').extract())
                    yield Request(linkw, callback = self.parse_details, meta={'category':category})


        nxt_pg = ''.join(sel.xpath('//span[@class="f4"]/b[span[@class="astrix"]]//following-sibling::span/a/@href').extract())
        if nxt_pg:  
            if "http" not in nxt_pg: nxt_pg = "http://www.esuppliersindia.com" + nxt_pg
            yield Request(nxt_pg, callback = self.parse_other_links)

    def parse_details(self, response):
        sel = Selector(response)
        title = ''.join(sel.xpath('//table//td[contains(text(), "Company Name :")]/following-sibling::td[@class="text-f11"]//text()').extract())
        category = response.meta.get('category','')
        address = ''.join(sel.xpath('//table//td[contains(text(), "Address : ")]/following-sibling::td[@class="text-f11"]//text()').extract()).replace('\n','').replace('\t','').replace('\r','').encode('utf8')
        con_person = ''.join(sel.xpath('//table//td[contains(text(), "Contact Person : ")]/following-sibling::td[@class="text-f11"]//text()').extract()).replace('\n','').replace('\t','').replace('\r','').encode('utf8')
        phone = ''.join(sel.xpath('//table//td[contains(text(), "Phone : ")]/following-sibling::td[@class="text-f11"]//text()').extract())
        mobile = ''.join(sel.xpath('//table//td[contains(text(), "Mobile : ")]/following-sibling::td[@class="text-f11"]//text()').extract())
        fax = ''.join(sel.xpath('//table//td[contains(text(), "Fax : ")]/following-sibling::td[@class="text-f11"]//text()').extract())
        #header = ['TITLE','ADDRESS','PH_NUM','CATEGORY','FAX','MOBILE','CONTACT_PERSON']
        #self.empt_dict.update({address:[title,address, phone, category,fax, mobile, con_person]})
        if "Bengaluru" in address:
            self.empt_dict.update({address:[title,address, phone, category,fax, mobile, con_person]})
            item = []
            item.append(title)
            item.append(address)
            item.append(phone)
            item.append(category)
            item.append(fax)
            item.append(mobile)
            item.append(con_person)


