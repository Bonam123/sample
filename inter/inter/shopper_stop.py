import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from ast import literal_eval
import json
import re


class Shoppers_stop(scrapy.Spider):
    name = 'shopper_stop'
    """ Inserting the url """
    start_urls = ["https://www.shoppersstop.com/p-204564407_9204/colorChange?colorCode=204564407_9204"]
    handle_httpstatus_list=[403]


    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//ul[@class="variant_size_ulClass"]//li')
        for node in nodes:
            selection = ''.join(node.xpath('.//input[@id="sizeVarInStock"]//@value').extract())
            if selection == "true":
                modle_size_id = ''.join(node.xpath('.//input[@class="variantSizeCode"]//@value').extract())
                set_cookies = response.headers.get('Set-Cookie','')
                csrf_token = ''.join(response.xpath('//div[@class="user-container user-icons log-member"]/input[@id="ajaxCSRF"]/@value').extract())
                """ Requesting cookies dynamically """
                cookies={}
                cookie = literal_eval(json.loads(json.dumps(str(response.headers)))).get('Set-Cookie', []) 
                for i in cookie:
                    data_key = i.split(';')[0]
                    if data_key:
                        try: key, val = data_key.split('=', 1)
                        except : continue
                        cookies.update({key.strip():val.strip()})

                headers = { 
                    'origin': 'https://www.shoppersstop.com',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9,te;q=0.8',
                    'x-requested-with': 'XMLHttpRequest',
                    'save-data': 'on',
                    'pragma': 'no-cache',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'accept': '*/*',
                    'cache-control': 'no-cache',
                    'authority': 'www.shoppersstop.com',
                    'referer': response.url,
                }                  
                prod_code = ''.join(re.findall('=(.\d+)_',response.url))
                data = { 
                  'qty': '1',
                  'baseProductCode': prod_code,
                  'productCodePost': modle_size_id,
                  'CSRFToken': csrf_token,
                }   
                yield FormRequest("https://www.shoppersstop.com/cart/add", callback =self.parse_cart, headers=headers,cookies=cookies,formdata=data,meta={'headers':headers})

    def parse_cart(self, response): 
        headers  = response.meta.get('headers','')
        yield Request('https://www.shoppersstop.com/cart',callback=self.parse_details, headers=headers)


    def parse_details(self, response): 
        size = response.xpath('//input[@name="sizeProductCode"]/@value').extract()
        product = response.xpath('//ul[@class="shop-listing cartListing"]//li[@class="clearfix"]//div[@class="pro-name"]/a/text()').extract()
        print size, product

