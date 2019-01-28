import scrapy
from scrapy.http import Request,FormRequest
import urllib
import json


class Purplle(scrapy.Spider):
    name = 'purplle'

    def start_requests(self):
        url = "https://www.purplle.com/search?q={0}".format('Hair fall shampoo')
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        headers = {
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://www.purplle.com/search?q=Hair%20fall%20shampoo',
                'Save-Data': 'on',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',  }
        pg_id = '1'
        if "api/shop/items" in response.url:
            pg_id = response.meta.get('pg_id','')
            pg_id = int(pg_id) + 1
        params = (
                ('list_type', 'search'),
                ('custom', ''),
                ('list_type_value', 'Hair fall shampoo'),
                ('page', str(pg_id)),
                ('sort_by', 'rel'),
                ('elite', '0'),
            )

        if "api/shop/items" in response.url:
            import pdb;pdb.set_trace()
            j_data = json.loads(response.body)
            node_ = j_data.get('items','')
            status = j_data.get('status','')
            #pg_id = response.meta.get('pg_id','')
            #pg_id = int(pg_id) + 1
            for node in node_:
                brand = node.get('brand_name','')
            if "Error".lower() not in status:
                import pdb;pdb.set_trace()
                url_ = 'https://www.purplle.com/api/shop/itemsv3?'+urllib.urlencode(params)
                yield Request(url_, callback=self.parse, headers=headers,meta={'pg_id':pg_id})
        else:
            url_ = 'https://www.purplle.com/api/shop/itemsv3?'+urllib.urlencode(params)
            yield Request(url_, callback=self.parse, headers=headers,meta={'pg_id':pg_id})

