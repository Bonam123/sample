from selenium import webdriver
from scrapy.selector import Selector

#driver = webdriver.Remote()
def driver_details():
    driver = webdriver.Firefox()
    driver.get("http://www.buzzinga.com/")
    html = driver.page_source
    sel = Selector(text=html)
    import pdb;pdb.set_trace()
    title = sel.xpath('//a[@title="Quantify the Social"]/@href').extract()
    main_details(title)
    driver.quit()

def main_details(title):
    import pdb;pdb.set_trace()
    print title    
   
if __name__ == '__main__':
    obj = driver_details()
