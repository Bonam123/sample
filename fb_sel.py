from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import scrapy
from scrapy.selector import Selector
import os
import  time
from datetime import datetime
import logging.handlers
import traceback

loggers = {}

def open_driver():
    display = Display(visible=1, size=(800,600))
    display.start()
    chrome_options = webdriver.ChromeOptions()
    #options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-extensions")
    #options.add_argument('--headless')
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver.maximize_window()
    return display, driver

def close_driver(display, driver):
    try:
        display.quit()
        driver.stop()
        #display.stop_client()
        #driver.stop()
    except Exception as exe:
        process_logger.debug(str(traceback.format_exc()))
    	process_logger.debug("Exception while closing driver.")
        pass

def myLogger(name):
    log_path = os.path.abspath('logs/')
    try:
        os.mkdir(log_path)
    except:
        pass
    global loggers
    path = "logs/fb_sel_%s_%s.log"
    if loggers.get(name):
        return loggers.get(name)

    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        now = datetime.now()
        handler = logging.FileHandler(path % (name, now.strftime("%Y-%m-%d")))
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(funcName)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        loggers.update(dict(name =  logger))
        return logger
process_logger = myLogger('process')


def start_processing(credintials):
    username = credintials.get('username','')
    password = credintials.get('password','')
    display, driver = open_driver()
    login_status = login_fb(driver, display, username, password)
    driver.find_element_by_css_selector('a[class="_y-c"]').click()
    driver.find_element_by_css_selector('a[data-testid="left_nav_item_Groups"]').click()
    #driver.implicitly_wait(50)
    time.sleep(50)
    driver.find_element_by_xpath('//div[@class="_ohe lfloat"]').click()
    time.sleep(50)
    discover_urls = driver.find_elements_by_xpath('//div[@class="_4-jm"]//div[@class="_266w"]//a')
    time.sleep(50)
    for url in discover_urls:
        time.sleep(50)
        main_url = url.get_attribute('href')
        time.sleep(10)
        print main_url
        final_data(driver, display, main_url)

def final_data(driver, display, main_url):
    driver.implicitly_wait(5)
    driver.find_element_by_id("userNavigationLabel").click()
    driver.find_element_by_xpath('//li[@class="_54ni navSubmenu _6398 _64kz __MenuItem"]//a').click()
    time.sleep(10)
    close_driver(driver, display)

def login_fb(driver, display, username, password):
    driver.get("https://www.facebook.com/")
    login_status = 0
    wait_driver = WebDriverWait(driver, 5)

    try:
       driver.find_element_by_id("email").send_keys(username)
       driver.find_element_by_id("pass").send_keys(password)
       driver.find_element_by_css_selector('input[value="Log In"]').click()
    except:
        invalid_login = ''


if __name__ == '__main__':
    credintials = {"username":"mailofme25@gmail.com", "password":"kittunikku"}
    obj = start_processing(credintials)

        
