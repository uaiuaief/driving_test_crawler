import os
import time
import headers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from captcha_solver import solver
from config import DRIVING_LICENCE_NUMBER, TEST_REF


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
    TEST_CENTER = "worksop"

    #@close_driver
    def get_data_sitekey(self, driver=None):
        options = Options()
        profile = webdriver.FirefoxProfile()

        user_agent = headers.get_user_agent()
        profile.set_preference("general.useragent.override", user_agent)
        
        driver = webdriver.Firefox(profile, options=options)

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
        driver.execute_script(f'onCaptchaFinished("{solution}")')

        driver.switch_to.default_content()
        #post recaptcha solving
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="main_c"]')))
            
        except:
            print('no queue')
            driver.switch_to.default_content()
            
        licence_number_textfield = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="driving-licence-number"]'))
                )


        #licence_number_textfield = driver.find_element_by_xpath('//input[@id="driving-licence-number"]')
        reference_number_textfield = driver.find_element_by_xpath('//input[@id="application-reference-number"]')
        continue_button = driver.find_element_by_xpath('//input[@id="booking-login"]')

        licence_number_textfield.send_keys(DRIVING_LICENCE_NUMBER)
        time.sleep(2)
        reference_number_textfield.send_keys(TEST_REF)
        time.sleep(10)
        continue_button.click()

        #LOGGED IN
        
        change_date_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="date-time-change"]')))

        change_date_button.click()

        earliest_date_radial_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="test-choice-earliest"]')))

        earliest_date_radial_button.click()
        earliest_date_radial_button.submit()
         
        change_date_main_div = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="page"]')))

        data_journey = change_date_main_div.get_attribute('data-journey')

        if data_journey == "pp-change-practical-driving-test-public:choose-alternative-test-centre":
            print("no available dates")
            return
        elif data_journey == "pp-change-practical-driving-test-public:choose-available-test":
            print("CHOOSE DATE PAGE")


            




    
    def get_captcha_solution(self, data_sitekey):
        print('solving')
        result = solver.recaptcha(sitekey=data_sitekey, url=self.URL)
        print('solved')

        return result.get('code')
        #return "123456"



