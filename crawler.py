import sys
import os
import time
import requests
import pprint
import headers
import json
import api_integration as API
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from captcha_solver import solver
from config import logger
import models


def close_driver(func):
    options = Options()
    #options.add_argument('--headless')
    #options.add_argument(f'user-agent={get_user_agent()}')

    def inner_function(self):
        with webdriver.Firefox(options=options) as driver:
            return func(self, driver)

    return inner_function


class DVSACrawler:
    WAIT_QUEUE_PRESENCE_TIME = 20
    MAIN_WAITING_TIME = 60
    WAIT_ON_QUEUE_TIME = 180

    URL = "https://driverpracticaltest.dvsa.gov.uk/login"
    CHANGE_TEST_CENTER = True

    driver = None

    def __init__(self, proxy=None):
        r = requests.get('http://localhost:8000/api/customers/SINHA955238IA9WL/')
        self.customer = models.Customer(r.json())
        self.proxy = proxy
        logger.debug(self.customer)


    def scrape(self):
        if self.proxy:
            logger.info(f"Proxy: {self.proxy}")
            webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                    "httpProxy": self.proxy,
                    "ftpProxy": self.proxy,
                    "sslProxy": self.proxy,
                    "proxyType": "MANUAL",
                    }
        else:
            logger.info(f"No Proxy")

        
        #with webdriver.Firefox(self.get_profile(), options=self.get_options()) as driver:
        if True:
            driver = webdriver.Firefox(self.get_profile(), options=self.get_options())
            self.driver = driver

            self.driver.get(self.URL)

            if self.is_ip_banned():
                return

            self.solve_captcha()
            self.login()
            self.go_to_change_date_page()

            ##

            earliest_date_radial_button = WebDriverWait(driver, self.MAIN_WAITING_TIME).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="test-choice-earliest"]')))

            earliest_date_radial_button.click()
            earliest_date_radial_button.submit()

#            change_date_main_div = WebDriverWait(driver, 20).until(
#                    EC.presence_of_element_located((By.XPATH, '//div[@id="page"]')))
#
#            data_journey = change_date_main_div.get_attribute('data-journey')
#            print(data_journey)

            if not self.are_there_available_dates():
                logger.debug("there are no available dates")
                if self.CHANGE_TEST_CENTER:
                    logger.info(f"changing test center to {self.customer.main_test_center.name}")
                    self.change_test_center()
                else:
                    return


            url = f'http://localhost:8000/api/add-available-dates/{self.customer.main_test_center.name}'
            payload = self.get_dates()

            #logger.debug(payload)

            r = requests.post(url, json=payload)
            #logger.debug(r.status_code)

            #calendar
#            if data_journey == "pp-change-practical-driving-test-public:choose-alternative-test-centre":
#                print("no available dates")
#                if self.CHANGE_TEST_CENTER:
#                    print(f"changing test center to {self.TEST_CENTER}")
#                    self.change_test_center()
#                return
#            elif data_journey == "pp-change-practical-driving-test-public:choose-available-test":
#                print("CHOOSE DATE PAGE")
#
    def get_profile(self):
        user_agent = headers.get_user_agent()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',False)
        profile.set_preference("media.peerconnection.enabled", False)
        profile.set_preference("general.useragent.override", user_agent)
        profile.update_preferences()

        return profile

    def get_options(self):
        options = Options()

        return options

    def is_customer_info_valid(self):
        options = Options()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',False)
        profile.set_preference("media.peerconnection.enabled", False)
        profile.update_preferences()

        user_agent = headers.get_user_agent()
        profile.set_preference("general.useragent.override", user_agent)
        
        with webdriver.Firefox(profile, options=options) as driver:
            self.driver = driver

            self.driver.get(self.URL)

            self.solve_captcha()
            self.login()

            try:
                WebDriverWait(driver, self.MAIN_WAITING_TIME).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@data-journey="pp-change-practical-driving-test-public:change-booking"]')))

                #API.validate_customer_info('1')
                return True
            except TimeoutException as e:
                #API.invalidate_customer_info('1')
                return False

    def are_there_available_dates(self):
        change_date_main_div = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="page"]')))

        data_journey = change_date_main_div.get_attribute('data-journey')

        if data_journey == "pp-change-practical-driving-test-public:choose-available-test":
            return True
        #else data_journey == "pp-change-practical-driving-test-public:choose-alternative-test-centre":
        else:
            return False
    
    def to_military_time(self, time):
        return datetime.strptime(time, '%I:%M%p').strftime('%H:%M')

    def get_dates(self):
        slot_picker_ul = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@class="SlotPicker-days"]')))

        available_days = slot_picker_ul.find_elements_by_tag_name('li')
        
        dates = {}
        #logger.info("available days: ", len(available_days))
        for available_day in available_days:
            labels = available_day.find_elements_by_tag_name('label')
            date = available_day.get_attribute('id')
            date = date[5:]
            #logger.info("getting date :", date)
            print(f"getting date: {date}")
            for label in labels:
                time_ = label.find_element_by_xpath('.//strong[@class="SlotPicker-time"]').get_attribute('innerHTML')

                print("getting time: ", time_)
                #dates.append(f"{date} :: {time}")
                time_ = self.to_military_time(time_)

                if not dates.get(date):
                    dates[date] = [time_]
                else:
                    dates[date].append(time_)

        #pprint.pprint(dates)
        return {'dates' : dates}
    
    def change_test_center(self):
        change_button = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="change-test-centre"]')))
        
        change_button.click()

        test_center_input = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="test-centres-input"]')))

        test_center_input.clear()
        test_center_input.send_keys(self.customer.main_test_center.name)
        test_center_input.submit()

        test_center_list = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@class="test-centre-results"]')))

        test_center_list.find_element_by_link_text(self.customer.main_test_center.name).click()



    def solve_captcha(self):
        iframe = self.driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
        self.driver.switch_to.frame(iframe)

        element = self.driver.find_element_by_xpath('//div[@class="g-recaptcha"]')
        sitekey = element.get_attribute('data-sitekey')

        solution = self.get_captcha_solution(sitekey)
        print(solution)

        text_field = self.driver.find_element_by_xpath('//textarea[@class="g-recaptcha-response"]')
        self.driver.execute_script(f"arguments[0].innerText = '{solution}'", text_field)
        self.driver.execute_script(f'onCaptchaFinished("{solution}")')

        self.driver.switch_to.default_content()

    def login(self):
        try:
            WebDriverWait(self.driver, self.WAIT_QUEUE_PRESENCE_TIME).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@id="main_c"]')))
        except:
            logger.info('no queue')
            self.driver.switch_to.default_content()

        licence_number_textfield = WebDriverWait(self.driver, self.WAIT_ON_QUEUE_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="driving-licence-number"]')))

        reference_number_textfield = self.driver.find_element_by_xpath('//input[@id="application-reference-number"]')
        continue_button = self.driver.find_element_by_xpath('//input[@id="booking-login"]')

        licence_number_textfield.send_keys(self.customer.driving_licence_number)
        reference_number_textfield.send_keys(self.customer.test_ref)
        continue_button.click()

    def go_to_change_date_page(self):
        change_date_button = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="date-time-change"]')))

        change_date_button.click()

    
    def get_captcha_solution(self, data_sitekey):
        logger.info('Solving Captcha')
        result = solver.recaptcha(sitekey=data_sitekey, url=self.URL)
        logger.info('Captcha Solved')

        return result.get('code')

    def is_ip_banned(self):
        iframe = self.driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
        self.driver.switch_to_frame(iframe)
        try:
            error = self.driver.find_element_by_xpath('//div[@class="error-title"]')
            if error.get_attribute('textContent') == 'Access denied':
                logger.error('Ip is banned')
                return True
            logger.debug('Ip is not banned')
            return False
        except:
            logger.debug('Ip is not banned')
            return False
        finally:
            self.driver.switch_to.default_content()




