import requests

headers = {
    'cookie': ' ROUTEID=.node2; JSESSIONID=B2E46EFEDACDE89347B3EE9D9137B9C9;',
    'origin': 'https://www.shoppersstop.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'accept': '*/*',
    'cache-control': 'no-cache',
    'referer': 'https://www.shoppersstop.com/p-203899558_9212/colorChange?colorCode=203899558_9212&currentPosition=1&searchQueryUrl=https%3A%2F%2Fwww.shoppersstop.com%2Fmen-new-arrivals%2Fc-A1060&totalResultVal=2913&searchPageType=category',
}

data = {
  'qty': '1',
  'baseProductCode': '203899558',
  'productCodePost': '203899645',
  'CSRFToken': '41d524d2-da62-469f-b479-4dd0ae71c396'
}

response = requests.post('https://www.shoppersstop.com/cart/add', headers=headers, data=data)
