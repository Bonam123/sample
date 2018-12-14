from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime, time


def start_processing():
    driver = webdriver.Chrome() #Open Chrome driver
    driver.get("http://credits.headrun.com/login/?next=/")
    time.sleep(3)
    driver.maximize_window() #Maximizing
    #Passing Credintials
    driver.find_element_by_id("id_username").send_keys("amrutha")
    driver.find_element_by_id("id_password").send_keys("amrutha123")
    driver.find_element_by_css_selector('input[type="submit"]').click()
    driver.find_element_by_css_selector('option[value="amrutha"]').click() #Selecting amrutha from dropdown list
    time.sleep(3)
    driver.find_element_by_link_text("See Global Transfers").click() #clicking global transfers link
    time.sleep(3)
    driver.find_element_by_css_selector('span[class="nextprev"]').click() #next page navigation
    time.sleep(3)
    driver.find_element_by_css_selector('a[rel="nofollow"]').click()
    driver.find_element_by_link_text("Overview").click()

    time.sleep(5)
    driver.find_element_by_link_text("Logout").click() # Logout from the link
    time.sleep(3)
    driver.quit()




if __name__ == '__main__':
    obj = start_processing()

        
