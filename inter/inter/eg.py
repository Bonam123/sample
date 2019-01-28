import scrapy
#import requests
import re

class EG(scrapy.Spider):
    name = "eg1"
    start_urls = ['https://www.shoppersstop.com/haute-curry-womens-tie-up-neck-printed-churidar-suit/p-203566837']

    def parse(self, response):
        import pdb;pdb.set_trace()
        cookies = response.headers.get('Set-Cookie','')
        j_session = ''.join(re.findall('JSESSIONID=(.*?) \Path',cookies))
        j_session = j_session.replace(';','')
        csrf_token = ''.join(response.xpath('//div[@class="user-container user-icons log-member"]/input[@id="ajaxCSRF"]/@value').extract())
        cookies={}
        cookie = literal_eval(json.loads(json.dumps(str(headers)))).get('Set-Cookie', [])
        for i in cookie:
            data_key  = i.split(';')[0]
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
            'referer': 'https://www.shoppersstop.com/haute-curry-womens-tie-up-neck-printed-churidar-suit/p-203566837',
        }

        data = {
          'qty': '1',
          'baseProductCode': '203566837',
          'productCodePost': '203566842',
          'CSRFToken': csrf_token,
        }
        response = requests.post('https://www.shoppersstop.com/cart/add', headers=headers, data=data)

