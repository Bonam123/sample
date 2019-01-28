import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

class Udaya_IN(scrapy.Spider):
    name = "udaya_vani"
    start_urls = ['https://www.udayavani.com/']

    def parse(self, response):
        sel = Selector(response)
        categories = response.xpath('//div[@class="views-field views-field-name"]/span[@class="field-content"]/a/@href').extract()
        for cat in categories:
            if "http" not in cat: cat = "https://www.udayavani.com" + cat
            print cat
            yield Request(cat, callback =self.parse_links)

    def parse_links(self, response):
        sel = Selector(response)
        links = response.xpath('//div[contains(@class, "views-row views-row-")]//div[@class="field-content"]/a/@href').extract()
        for link in links:
            if "http" not in link: link = "https://www.udayavani.com" + link
            print link
            yield Request(link, callback =self.parse_details)

        nxt_pg = ''.join(response.xpath('//a[@title="Go to next page"]/@href').extract())
        if nxt_pg:
            if "http" not in nxt_pg: nxt_pg = "https://www.udayavani.com" + nxt_pg
            yield Request(nxt_pg, callback =self.parse_links)






        import pdb;pdb.set_trace()

