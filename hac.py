import requests
from scrapy.selector import Selector


headers = {
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'origin': 'https://hackforums.net',
    'upgrade-insecure-requests': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #'referer': 'https://hackforums.net/member.php?action=login',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,te;q=0.8',
    'authority': 'hackforums.net',
}
#response = requests.get('https://hackforums.net/member.php', headers=headers)
response = requests.get('https://hackforums.net/member.php?action=login',headers=headers)
headers = { 
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'origin': 'https://hackforums.net',
    'upgrade-insecure-requests': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'referer': 'https://hackforums.net/member.php?action=login',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,te;q=0.8',
    'authority': 'hackforums.net',
}

cookies = response.cookies.get_dict()
data = {
  'username': 'kerspdr',
  'password': 'Inqspdr2018.',
  'quick_gauth_code': '',
  'remember': 'yes',
  'submit': 'Login',
  'action': 'do_login',
  'url': 'https://hackforums.net/'
}
#data = json.dumps(data)
#response = requests.post('https://hackforums.net/member.php', headers=headers, data=data,cookies=cookies)
response = requests.post('https://hackforums.net/member.php', data=data)

