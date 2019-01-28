import requests
import time
import urllib
import json

class Purplle(object):

    def main(self):
        search_key = ['Hair fall shampoo','Shampoo','Conditioner']
        """ Iterating over the keywords """
        for keyword in search_key:
            url = "https://www.purplle.com/search?q={0}".format(keyword)
            """ fetching results from the main url """
            response_data = requests.get(url).text
            self.urls(response_data,url,keyword)
    def urls(self, response_data,url,keyword):
        headers = {
            'pragma': 'no-cache',
            'cookie': '  purpllesession=%2BuThNQ8zz670qZgVlki7Wo%2F0MaKKXMF84g9BLxF9pvuTpOePK%2BKBYddPMtqKcbPZcf9EoFFWVMRF0J%2BLGEb%2FfgzyNN9vlufi%2Fm8H8%2FKTSlcJrarmhOJ%2BSXeE3T8zVlOMNw2L78OquK1HQl9UCnfNJ5SSG9ene%2BlGjvg%2FSJtlhPqCX1JUGtKJPDL5ODq3BU4fCawMtNbT50GAxuDj4oA6uLewrjAURYa52dQsdm31SyB8cybcbt0fASQqNAI4Nm5fdAYmRotPYLba5J2%2B67xxgqyK38Ew0rW%2B3VxM7Z14xwlT52Zv1CMz1tPwe01p3F5QO%2F9wiAikm%2B%2F%2BKMukFhjsAEXwaduD%2FR2WE1rZ6G7WXs9%2Foj5k9Dop7Tml8r5Fn0c6MCK98FcSLjLSELKTnqiIPSUZu0w6JODhv4NWKgblalQ%3D;',

            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,te;q=0.8',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'cache-control': 'no-cache',
            'authority': 'www.purplle.com',
        }
        for i in range(1, 10):
            pg_id = str(i)
            params = (
                    ('list_type', 'search'),
                    ('custom', ''),
                    ('list_type_value', keyword),
                    ('page', str(pg_id)),
                    ('sort_by', 'rel'),
                    ('elite', '0'), 
                )

            response = requests.get('https://www.purplle.com/api/shop/itemsv3', headers=headers, params=params)
            print response.url
            if "api/shop/items" in response.url:
                j_data = json.loads(response.text)
                node_ = j_data.get('items','')
                status = j_data.get('status','')
                brand_list = []
                final_list = []
                final_dict = {}
                item_dict = []
                if "error" in status.lower(): continue

                for index, node in enumerate(node_):
                    brand = node.get('brand_name','')
                    brand_list.append([brand,index])
                for item in brand_list:
                    if "professionnel" in item[0].lower() or 'dove' in item[0].lower() or "tressemme" in item[0].lower():
                        final_list.append(item)
                loreal_position = [asa for asa in final_list if "oreal professionnel" in asa[0].lower()]
                dove_position = [asa for asa in final_list if "dove" in asa[0].lower()]
                tressemme_position = [asa for asa in final_list if "tressemme" in asa[0].lower()]
                try:
                    loreal_position = loreal_position[0][1]
                except:
                    loreal_position = ''
                try:
                    dove_position = dove_position[0][1]
                except:
                    dove_position = ''
                try:
                    tressemme_position = tressemme_position[0][1]
                except:
                    tressemme_position = ''
                tt_list = []
                inside_dict = {}
                inside_dict.update({"keyword":keyword})
                inside_dict.update({"position":{"loreal":loreal_position, "tresemme":tressemme_position, "dove":dove_position}})
                tt_list.append(inside_dict)
                total_dict = {"result":tt_list}

                print total_dict
                #if "error" not in status.lower(): continue

if __name__ == '__main__':
    Purplle().main()
