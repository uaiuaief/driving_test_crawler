import sys
import os
import time
import requests
import pprint
import headers
import json
import api_integration as API
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from captcha_solver import solver
from config import logger
import models


def wait_input():
    if input('press enter to continue'):
        pass

class DVSACrawler:
    WAIT_QUEUE_PRESENCE_TIME = 15
    MAIN_WAITING_TIME = 20
    WAIT_ON_QUEUE_TIME = 180
    WAIT_FOR_CAPTCHA_TIME = 10

    URL = "https://driverpracticaltest.dvsa.gov.uk/login"
    CHANGE_TEST_CENTER = True

    driver = None
    captcha_solved = False

    display_slots_script = "document.getElementsByClassName('SlotPicker-timeSlots')[0].style.display = 'block'; els = document.getElementsByClassName('SlotPicker-day'); arr = Array.from(els); arr.map((each) => each.style.display = 'block');"

    def __init__(self, customer, proxy=None):
        #r = requests.get('http://localhost:8000/api/customers/SINHA955238IA9WL/')
        self.customer = customer
        self.proxy = proxy
        #self.proxy = None
        logger.debug(self.customer)

        if self.proxy:
            logger.info(f"Proxy: {self.proxy}")
            webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                    "httpProxy": self.proxy,
                    #"ftpProxy": self.proxy,
                    "sslProxy": self.proxy,
                    "proxyType": "MANUAL",
                    }
        else:
            logger.info(f"No Proxy")

    def scrape(self):
        with webdriver.Firefox(self.get_profile(), options=self.get_options()) as driver:
        #if True:
            #driver = webdriver.Firefox(self.get_profile(), options=self.get_options())
            self.driver = driver

            self.driver.get(self.URL)


            if self.is_ip_banned():
                return
            self.login()
            if self.is_ip_banned():
                return
            self.solve_captcha()
            if(self.is_test_cancelled()):
                return
            if(self.is_test_non_refundable()):
                return
            self.set_current_test_date()
            if self.is_ip_banned():
                return
            self.solve_captcha()
            self.go_to_change_date_page()
            if self.is_ip_banned():
                return
            self.solve_captcha()

            if self.is_ip_banned():
                return
            ##

            earliest_date_radial_button = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="test-choice-earliest"]')))

            earliest_date_radial_button.click()
            earliest_date_radial_button.submit()

            if self.is_ip_banned():
                return

            if self.are_there_available_dates():
                self.driver.execute_script(self.display_slots_script)
                self.auto_book()
            else:
                logger.debug("there are no available dates")
                for each in self.customer.test_centers:
                    time.sleep(5)
                    test_center_name = each.name
                    logger.info(f"changing test center to {test_center_name}")
                    self.change_test_center(test_center_name)

                    if self.is_ip_banned():
                        return
            
                    self.solve_captcha()

                    if self.are_there_available_dates():
                        self.driver.execute_script(self.display_slots_script)
                        self.auto_book(test_center=each)
                    else:
                        logger.debug("there are no available dates")

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
        options.add_argument('--headless')

        return options

    def is_test_cancelled(self):
        WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//section[@id="confirm-booking-details"]')))

        try:
            el = self.driver.find_element_by_xpath('//div[@class="contents"]/dl/dd[3]')
        except exceptions.NoSuchElementException:
            return False

        if el.get_attribute('textContent') == 'Cancelled':
            logger.info('test is cancelled, invalidating customer info')
            API.invalidate_customer_info(self.customer.id)
            return True
        else:
            return False

    def is_test_non_refundable(self):
        WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//section[@id="confirm-booking-details"]')))

        try:
            el = self.driver.find_element_by_xpath('//div[@class="contents"]/dl/dd[2]')
        except exceptions.NoSuchElementException:
            return False

        if el.get_attribute('textContent') == 'This test slot is non-refundable':
            logger.info("test date is non-refundable, can't change date")
            API.set_test_booked(self.customer.id)
            return True
        else:
            return False

    def is_customer_info_valid(self):
        with webdriver.Firefox(self.get_profile(), options=self.get_options()) as driver:
            self.driver = driver

            self.driver.get(self.URL)

            if self.is_ip_banned():
                raise Exception('ip is banned')
            self.login()
            if self.is_ip_banned():
                raise Exception('ip is banned')
            self.solve_captcha()

            for i in range(3):
                result = None
                try:
                    logger.info('waiting to know if it\'s logged in')
                    #WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                            #EC.presence_of_element_located((By.XPATH, '//div[@data-journey="pp-change-practical-driving-test-public:change-booking"]')))
                    WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@id="header-button-container"]')))
                    return True
                except TimeoutException as e:
                    logger.info('time out 1')
                    try:
                        logger.info('waiting to know if credentials are invalid')
                        WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                                EC.presence_of_element_located((By.XPATH, '//section[@class="error-summary formatting"]')))
                        return False
                    except TimeoutException as e:
                        logger.info('no error message, checking presence of login fields')
                        try:
                            WebDriverWait(self.driver, self.WAIT_ON_QUEUE_TIME).until(
                                    EC.presence_of_element_located((By.XPATH, '//input[@id="driving-licence-number"]')))
                            return False
                        except TimeoutException as e:
                            logger.info('time out 2, trying again')

            logger.info("unable to get an anwser, exiting script")

            return None

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

    def auto_book(self, test_center):
        slot_picker_ul = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@class="SlotPicker-days"]')))

        available_days = slot_picker_ul.find_elements_by_tag_name('li')
        
        dates = {}
        for available_day in available_days:
            labels = available_day.find_elements_by_tag_name('label')
            date = available_day.get_attribute('id')
            date = date[5:]
            if date:
                labels = available_day.find_elements_by_tag_name('label')

                for label in labels:
                    time_element = label.find_element_by_xpath('.//strong[@class="SlotPicker-time"]')
                    time_ = time_element.get_attribute('innerHTML')
                    time_ = self.to_military_time(time_)

                    logger.info(f"Found date: {date}, {time_}")

                    if self.can_test_be_booked(date, time_):
                        logger.info(f"Booking test:\nTest Center -> {test_center.name}")
                        logger.info(f"\nTest Day -> {date}")
                        logger.info(f"\nTest Time -> {time_}")

                        time_element.click()
                        time_element.submit()
                        continue_button = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                                EC.presence_of_element_located((By.XPATH, '//button[@id="slot-warning-continue"]')))

                        continue_button.click()

                        i_am_the_candidate_button = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                                EC.presence_of_element_located((By.XPATH, '//a[@id="i-am-candidate"]')))

                        i_am_the_candidate_button.click()

                        """DON'T CLICK THIS BUTTON OR IT WILL CHANGE THE CUSTOMER DATE"""
                        confirm_changes_button = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                                EC.presence_of_element_located((By.XPATH, '//input[@id="confirm-changes"]')))


                        confirm_changes_button.click()

                        API.send_test_found_email(data={
                            'user_id': self.customer.id,
                            'test_time': time_,
                            'test_date': date,
                            'test_center_id': test_center.id
                        })

                        return

    def is_time_within_range(self, time_found):
        time_object = datetime.strptime(time_found, "%H:%M").time()
        
        """
        Is the time that whas found BEFORE the initial time that the
        customer can go to the test?
        """
        if self.customer.earliest_time:
            if time_object >= self.customer.earliest_time:
                is_after_earliest_time = True
            else:
                is_after_earliest_time = False
        else:
            is_after_earliest_time = True


        """
        Is the time that was found AFTER the latest time that the
        customer can go to the test?
        """
        if self.customer.latest_time:
            if time_object <= self.customer.latest_time:
                is_before_latest_time = True
            else:
                is_before_latest_time = False
        else:
            is_before_latest_time = True


        if is_after_earliest_time and is_before_latest_time:
            return True
        else:
            logger.debug("Time not within range")
            return False

    def is_day_within_customer_date_range(self, date_found: str):
        earliest = datetime(
                self.customer.earliest_test_date.year,
                self.customer.earliest_test_date.month,
                self.customer.earliest_test_date.day,
                ).date()
        
        date_object = datetime.strptime(date_found, "%Y-%m-%d").date()

        """
        Is the day found BEFORE the customer earliest viable date?
        """
        if date_object < earliest:
            logger.debug("Date before customer date range")
            return False

        if not self.customer.latest_test_date:
            return True

        latest = datetime(
                self.customer.latest_test_date.year,
                self.customer.latest_test_date.month,
                self.customer.latest_test_date.day,
                ).date()

        """
        Is the day found AFTER the customer earliest viable date?
        """
        if date_object > latest:
            logger.debug("Date after customer date range")
            return False
        else:
            return True

    def is_day_within_refundable_range(self, date_found: str):
        date_object = datetime.strptime(date_found, "%Y-%m-%d").date()
        last_refundable_date = (datetime.today() + timedelta(days=5)).date()

        if date_object < last_refundable_date:
            logger.debug("Date not within refundable range")
            return False
        else:
            return True

    def is_day_after_recent_failure_date_limit(self, date_found: str):
        date_object = datetime.strptime(date_found, "%Y-%m-%d").date()

        if self.customer.recent_test_failure \
                and date_object < self.customer.recent_test_failure + timedelta(days=16):
                    logger.debug("Date not after recent failure limit")
                    return False
        else:
            return True

    def can_test_be_booked(self, date_found: str, time_found: str):
        if self.is_day_within_customer_date_range(date_found) \
                and self.is_day_within_refundable_range(date_found) \
                and self.is_day_after_recent_failure_date_limit(date_found) \
                and self.is_before_current_test_date(date_found, time_found) \
                and self.is_time_within_range(time_found):

                    return True
        else:
            return False

    def is_before_current_test_date(self, date_found: str, time_found: str):
        date_object = datetime.strptime(date_found, "%Y-%m-%d").date()
        time_object = datetime.strptime(time_found, "%H:%M").time()

        date_is_equal = date_object == self.customer.current_test_date.date()
        date_is_before = date_object < self.customer.current_test_date.date()
        time_is_before = time_object < self.customer.current_test_date.time()

        if date_is_before:
            return True
        elif date_is_equal and time_is_before:
            return True
        else:
            logger.debug("Date not before current test date")
            return False

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
    
    def change_test_center(self, test_center_name):
        change_button = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="change-test-centre"]')))
        
        WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.invisibility_of_element_located((By.XPATH, '//div[@class="system-busy"]')))
        #WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                #EC.invisibility_of_element_located((By.XPATH, '//div[@id="progress-bar"]')))
        #WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                #EC.invisibility_of_element_located((By.XPATH, '//li[@class="end-point"]')))

        change_button.click()

        test_center_input = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="test-centres-input"]')))

        test_center_input.clear()
        test_center_input.send_keys(test_center_name)
        test_center_input.submit()

        test_center_list = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@class="test-centre-results"]')))

        test_center_list.find_element_by_link_text(test_center_name).click()

    def find_captcha_element(self):
        if self.captcha_solved:
            return None

        logger.debug('Checking reCAPTCHA presence')
        try:
            captcha_iframe = WebDriverWait(self.driver, self.WAIT_FOR_CAPTCHA_TIME).until(
                    EC.presence_of_element_located((By.XPATH, '//iframe[@id="main-iframe"]')))

            return captcha_iframe
        except Exception as e:
            logger.info('No captcha')

            return None

    def solve_captcha(self):
        iframe = self.find_captcha_element()

        if not iframe:
            return

        self.driver.switch_to.frame(iframe)

        element = self.driver.find_element_by_xpath('//div[@class="g-recaptcha"]')
        sitekey = element.get_attribute('data-sitekey')

        text_field = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//textarea[@class="g-recaptcha-response"]')))

        solution = self.get_captcha_solution(sitekey)
        print(solution)

        self.driver.execute_script(f"arguments[0].innerText = '{solution}'", text_field)
        self.driver.execute_script(f'onCaptchaFinished("{solution}")')
       
        time.sleep(1)

        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except exceptions.NoAlertPresentException:
            logger.debug('no alert')

        self.captcha_solved = True
        self.driver.switch_to.default_content()

    def login(self):
        try:
            self.solve_captcha()
            logger.info('waiting queue presence')
            #WebDriverWait(self.driver, self.WAIT_QUEUE_PRESENCE_TIME).until(
                    #EC.presence_of_element_located((By.XPATH, '//div[@id="main_c"]')))
            WebDriverWait(self.driver, self.WAIT_QUEUE_PRESENCE_TIME).until(
                    EC.presence_of_element_located((By.XPATH, '//body[@class="queue"]')))
            logger.info('waiting on queue')
            self.solve_captcha()
        except Exception as e:
            logger.error(str(e))
            self.solve_captcha()
            logger.info('no queue')
            self.driver.switch_to.default_content()


        try:
            licence_number_textfield = WebDriverWait(
                self.driver, self.MAIN_WAITING_TIME).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@id="driving-licence-number"]')))
        except Exception as e:
            self.solve_captcha()

        licence_number_textfield = WebDriverWait(
                self.driver, self.WAIT_ON_QUEUE_TIME).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@id="driving-licence-number"]')))

        self.solve_captcha()

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
        try:
           # iframe = WebDriverWait(self.driver, self.5).until(
           #         EC.presence_of_element_located((By.XPATH, '//iframe[@id="main-iframe"]')))
            iframe = self.driver.find_element_by_xpath('//iframe[@id="main-iframe"]')

        except Exception as e:
            logger.info('Not banned')
            return False

        self.driver.switch_to_frame(iframe)
        try:
            error = self.driver.find_element_by_xpath('//div[@class="error-title"]')
            if error.get_attribute('textContent') == 'Access denied':
                logger.error('Ip is banned')
                API.ban_proxy(self.proxy)

                return True
            logger.debug('Ip is not banned')
            return False
        except:
            logger.debug('Ip is not banned')
            return False
        finally:
            self.driver.switch_to.default_content()

    def set_current_test_date(self):
        el = WebDriverWait(self.driver, self.MAIN_WAITING_TIME).until(
                EC.presence_of_element_located((By.XPATH, '//section[@id="confirm-booking-details"]/section[1]/div/dl/dd[1]')))

        el_text = el.get_attribute('textContent')
        el_text = f"{el_text}+0100"

        #date_obj = datetime.strptime(el_text, "%A %d %B %Y %I:%M%p")
        date_obj = datetime.strptime(el_text, "%A %d %B %Y %I:%M%p%z")
        date_str = format(date_obj, "%Y-%m-%dT%H:%M:%S%z")

        self.customer.current_test_date = date_str

        API.set_customer_current_test_date(self.customer.id, self.customer.current_test_date)
        



