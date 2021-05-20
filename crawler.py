import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from captcha_solver import solver
import headers


def close_driver(func):
    options = Options()
    #options.add_argument('--headless')
    #options.add_argument(f'user-agent={get_user_agent()}')

    def inner_function(self):
        with webdriver.Firefox(options=options) as driver:
            return func(self, driver)

    return inner_function


class DVSACrawler:
    URL = "https://driverpracticaltest.dvsa.gov.uk/login"

    #@close_driver
    def get_data_sitekey(self, driver=None):
        options = Options()
        profile = webdriver.FirefoxProfile()
        user_agent = headers.get_user_agent()
        print(user_agent)
        profile.set_preference("general.useragent.override", user_agent)
        
        driver = webdriver.Firefox(profile, options=options)
        driver._client.set_header_overrides(headers='blabla')

        if not driver:
            raise TypeError("driver can't be of type None, decorate this function with `@close_driver`")

        driver.get(self.URL)

        iframe = driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
        driver.switch_to.frame(iframe)

        element = driver.find_element_by_xpath('//div[@class="g-recaptcha"]')
        sitekey = element.get_attribute('data-sitekey')

        solution = self.get_captcha_solution(sitekey)

        text_field = driver.find_element_by_xpath('//textarea[@class="g-recaptcha-response"]')
        driver.execute_script(f"arguments[0].innerText = '{solution}'", text_field)
        text_field.submit()

#        recaptcha_iframe = driver.find_element_by_xpath('//iframe[@title="reCAPTCHA"]')
#        driver.switch_to.frame(recaptcha_iframe)
#
#        checkbox = driver.find_element_by_xpath('//span[@id="recaptcha-anchor"]')
#        checkbox.click()
        #text_field.send_keys(solution)
        
    
    def get_captcha_solution(self, data_sitekey):
        print('solving')
        #result = solver.recaptcha(sitekey=data_sitekey, url=self.URL)

        #return result.get('code')
        return "123456"



