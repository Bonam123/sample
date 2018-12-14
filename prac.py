import scrapy

class Hel(scrapy.Spider):
    name = "prac"
    start_urls = ["https://www.hellboundhackers.org/forum/contribute_to_the_newsletter-75-14910_0.html"]

    def parse(self, response):
        nodes = response.xpath('//tr')
        for node in nodes:
            text = node.xpath('.//td[@class="tbl1"]//text()').extract()

            import pdb;pdb.set_trace()


