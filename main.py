import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC

#This example requires Selenium WebDriver 3.13 or newer
#driver = webdriver.Firefox(executable_path = '/home/john/DrivingTest/geckodriver') 

def get_data_sitekey(driver):
    driver.get("https://driverpracticaltest.dvsa.gov.uk/login")
    #driver.switch_to.frame(iframe)

    iframe = driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
    driver.switch_to.frame(iframe)

    element = driver.find_element_by_xpath('//div[@class="g-recaptcha"]')
    
    return element.get_attribute('data-sitekey')



firefox_options = Options()
firefox_options.add_argument('--headless')

with webdriver.Firefox(options=firefox_options) as driver:
    wait = WebDriverWait(driver, 2)
    #driver.get("https://www.gov.uk/change-driving-test")
    driver.get("https://driverpracticaltest.dvsa.gov.uk/login")

    get_data_sitekey(driver)
    
    #iframe = driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
    #driver.switch_to.frame(iframe)

    #recaptcha_iframe = driver.find_element_by_xpath('//iframe[@title="reCAPTCHA"]')
    #driver.switch_to.frame(recaptcha_iframe)

    #im_not_a_robot = driver.find_element_by_xpath('//span[@id="recaptcha-anchor"]')
    #im_not_a_robot.click()

    #print('clicked')
    #driver.implicitly_wait(4)
    #print(el.get_attribute('outerHTML'))

    #driver.switch_to.default_content()
    #iframe = driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
    #driver.switch_to.frame(iframe)

    #challenge_iframe = driver.find_element_by_xpath('//iframe[@title="recaptcha challenge"]')
    #print(challenge_iframe.get_attribute('outerHTML'))

    #driver.switch_to.frame(challenge_iframe)


    #print(iframe.get_attribute('outerHTML'))
    #print(driver.page_source)
    #q = driver.find_element_by_xpath('//div[@id="captcha"]')
    #q = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div[1]')

    #print(q.get_attribute('innerHTML'))

#    for iframe in elements:
#        #iframe.find_element_by_xpath("./child::*")
#        #print(iframe.get_attribute('outerHTML'))
#        q = iframe.find_element_by_xpath('//body')
#        print(q.get_attribute('innerHTML'))
#

    
    #print(driver.page_source)


