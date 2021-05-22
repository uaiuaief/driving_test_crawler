import os
import time
import headers
import pprint
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
    CHANGE_TEST_CENTER = True
    TEST_CENTER = "Worksop"

    driver = None

    def scrape(self):
        options = Options()
        profile = webdriver.FirefoxProfile()

        user_agent = headers.get_user_agent()
        profile.set_preference("general.useragent.override", user_agent)
        
        #with webdriver.Firefox(profile, options=options) as driver:
        if True:
            driver = webdriver.Firefox(profile, options=options)
            self.driver = driver

            self.driver.get(self.URL)

            if self.is_ip_banned():
                print('ip banned')
                return

            self.solve_captcha()
            self.login()
            self.go_to_change_date_page()

            ##

            earliest_date_radial_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="test-choice-earliest"]')))

            earliest_date_radial_button.click()
            earliest_date_radial_button.submit()

            change_date_main_div = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@id="page"]')))

            data_journey = change_date_main_div.get_attribute('data-journey')
            print(data_journey)

            ##
            print(f"changing test center to {self.TEST_CENTER}")


            self.change_test_center()

            self.get_dates()

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
    def get_dates(self):
        slot_picker_ul = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@class="SlotPicker-days"]')))

        available_days = slot_picker_ul.find_elements_by_tag_name('li')
        
        dates = {}
        print("available days: ", len(available_days))
        for available_day in available_days:
            labels = available_day.find_elements_by_tag_name('label')
            date = available_day.get_attribute('id')
            print("getting date :", date)
            for label in labels:
                time = label.find_element_by_xpath('.//strong[@class="SlotPicker-time"]').get_attribute('innerHTML')
                #print("getting time :", time)
                #dates.append(f"{date} :: {time}")
                if not dates.get(date):
                    dates[date] = [time]
                else:
                    dates[date].append(time)

        pprint.pprint(dates)


    
    def change_test_center(self):
        change_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="change-test-centre"]')))
        
        change_button.click()

        test_center_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="test-centres-input"]')))

        test_center_input.clear()
        test_center_input.send_keys(self.TEST_CENTER)
        test_center_input.submit()

        test_center_list = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@class="test-centre-results"]')))

        test_center_list.find_element_by_link_text(self.TEST_CENTER).click()



    def solve_captcha(self):
        iframe = self.driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
        self.driver.switch_to.frame(iframe)

        element = self.driver.find_element_by_xpath('//div[@class="g-recaptcha"]')
        sitekey = element.get_attribute('data-sitekey')

        solution = self.get_captcha_solution(sitekey)

        text_field = self.driver.find_element_by_xpath('//textarea[@class="g-recaptcha-response"]')
        self.driver.execute_script(f"arguments[0].innerText = '{solution}'", text_field)
        self.driver.execute_script(f'onCaptchaFinished("{solution}")')

        self.driver.switch_to.default_content()

    def login(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="main_c"]')))
        except:
            print('no queue')
            self.driver.switch_to.default_content()

        licence_number_textfield = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="driving-licence-number"]'))
                )

        reference_number_textfield = self.driver.find_element_by_xpath('//input[@id="application-reference-number"]')
        continue_button = self.driver.find_element_by_xpath('//input[@id="booking-login"]')

        licence_number_textfield.send_keys(DRIVING_LICENCE_NUMBER)
        reference_number_textfield.send_keys(TEST_REF)
        continue_button.click()

    def go_to_change_date_page(self):
        change_date_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="date-time-change"]')))

        change_date_button.click()

    
    def get_captcha_solution(self, data_sitekey):
        print('solving')
        result = solver.recaptcha(sitekey=data_sitekey, url=self.URL)
        print('solved')

        return result.get('code')
        #return "123456"

    def is_ip_banned(self):
        iframe = self.driver.find_element_by_xpath('//iframe[@id="main-iframe"]')
        self.driver.switch_to_frame(iframe)
        try:
            error = self.driver.find_element_by_xpath('//div[@class="error-title"]')
            if error.get_attribute('textContent') == 'Access denied':
                print('IP IS BANNED')
                return True
            print('not banned')
            return False
        except:
            print('not banned')
            return False
        finally:
            self.driver.switch_to.default_content()




