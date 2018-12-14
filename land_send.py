import scrapy
import json
import re
import time
import datetime
import shutil
import os
from optparse import OptionParser
from scrapy.selector import Selector
from selenium import webdriver
from scrapy.http import Request
import xlwt, xlrd
from scrapy.xlib.pydispatch import dispatcher
from openpyxl import Workbook
from scrapy import signals


class Land_send(scrapy.Spider):
    name = 'land_send'
    start_urls =['https://www.landsend.com']

    row_count = 1 
    def __init__(self):
        self.file_      =  xlwt.Workbook(encoding="utf-8")
        self.contain = self.file_.add_sheet("LAND_SEND_DATA")
        header = ['url', 'Title', 'Product_Details', 'Product_Description', 'colors', 'price', 'size', 'image', 'itemNumber']
        style           = "font: bold on"
        for i, row in enumerate(header):
            self.contain.write(0, i, row, xlwt.Style.easyxf(style))
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.file_.save("LAND_SEND.xlsx") 


    def parse(self, response):
        sel = Selector(response)
        """As in Scrapy not getting response, used Selenium for taking menu1"""
        driver = webdriver.Firefox()
        driver.get("https://www.landsend.com/")
        time.sleep(15)
	import pdb;pdb.set_trace()
