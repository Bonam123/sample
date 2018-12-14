import scrapy
from scrapy. selector import Selector
from scrapy. http import Request
import urllib
import re
import json

class Po(scrapy.Spider):
    name = "po"
    start_urls = ['https://issuu.com/search?q=australia']

    def parse(self, response):
        sel = Selector(response)
        sta_id = ''.join(response.xpath('//script[@type="application/javascript"]//text()').extract())
        state_id  =''.join(re.findall('state=(.*)",', sta_id))
        if "stream/api/publicationsearch/1/0/cont/" in  response.url:
            js_data  = json.loads(response.body)
            state_id = js_data['rsp']['_content']['continuation']
            state_id = state_id.replace(u'/call/stream/api/publicationsearch/1/0/cont/master-25?state=','')
            other_data = js_data['rsp']['_content']['stream']
            for item_ in other_data:
                main_data = item_.get('content','')
                un_ = main_data.get('ownerUsername','')
                pb_name = main_data.get('publicationName','')
                url = ''.join(re.findall('.*.com', response.url))
                link = url +'/'+un_+'/docs/'+pb_name
                import pdb;pdb.set_trace()
                print link
                #yield Request(link, callback = self.parse_details)

        params = (
                ('state', state_id),
                ('pageSize', '20'),
                ('format', 'json'),
        )
        url_ =  "https://issuu.com/call/stream/api/publicationsearch/1/0/cont/master-25?"+urllib.urlencode(params)
        import pdb;pdb.set_trace()
        yield Request(url_, callback= self.parse)
    

    def parse_details(self, response):
        sel = Selector(response)
        import pdb;pdb.set_trace()

