import scrapy
from scrapy.selector import Selector

class Indep(scrapy.Spider):
    name = 'indep'
    start_urls = ['https://en.wikipedia.org/wiki/32nd_Independent_Spirit_Awards']


    def parse(self, response):
        sel = Selector(response)
        award_title = 'Film Independent Spirit Awards'
        award_gid = 'WIKI1239235'
        year = '2017'
        location = "Santa Monica, California, United States"
        awrd_nodes = sel.xpath('//h3')
        for awrd_node in awrd_nodes:
            cat_link = ''.join(awrd_node.xpath('.//span[@class="mw-headline"]//a/@title').extract()) or ''.join(awrd_node.xpath('.//span[@class="mw-headline"]/@id').extract())
            if 'Films_with_multiple_nominations_and_awards' in cat_link: continue
            cat_nodes =  awrd_node.xpath('./following-sibling::ul[1]//li')
            program_link,persons,role = [],[],[]
            for cat_node in cat_nodes:
                print cat_link
                program_title = cat_node.xpath('./i/b/a/@href').extract() or cat_node.xpath('./i/b/a//text()').extract() or cat_node.xpath('.//li/b//i/a/@href').extract() or cat_node.xpath('./b/i/a/@href').extract() or cat_node.xpath('./b/i/a//text()').extract()
                if program_title:
                    program_link.extend(program_title)
                    winner_type = "winner"
                    person = cat_node.xpath('./b[i]//preceding-sibling::text()').extract()
                    persons.extend(person)
                    print person
                    print program_title
                    print winner_type
                    print "--------------"
                    import pdb;pdb.set_trace()
                else:
                    winner_type = "nominee"
                    program_title = cat_node.xpath('./i/a/@href').extract() or cat_node.xpath('./i/a/text() | ./i/text()').extract()
                    program_link.extend(program_title)
                    person = cat_node.xpath('./a/@href').extract() or cat_node.xpath('./a//text() | .//i//preceding-sibling::text()').extract()
                    persons.extend(person)

                    print program_title
                    print person
                    print winner_type
                    print "-------------2222-"
                    import pdb;pdb.set_trace()

