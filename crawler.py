import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


def close_driver(func):
    options = Options()
    options.add_argument('--headless')

    def inner_function(self):
        with webdriver.Firefox(options=options) as driver:
            return func(self, driver)

    return inner_function

class DVSACrawler:
    URL = "https://driverpracticaltest.dvsa.gov.uk/login"

    @close_driver
    def get_data_sitekey(self, driver=None):
        if not driver:
            raise TypeError("driver can't be of type None, decorate this function with `@close_driver`")

        driver.get(self.URL)

        iframe = driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
        driver.switch_to.frame(iframe)

        element = driver.find_element_by_xpath('//div[@class="g-recaptcha"]')

        return element.get_attribute('data-sitekey')
    
    def solve_captcha(self):
        pass



