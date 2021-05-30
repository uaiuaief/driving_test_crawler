import time
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import headers


proxies = []
with open('untested.txt', 'r') as f:
    for each in f.readlines():
        proxies.append(each.strip())


URL = "https://driverpracticaltest.dvsa.gov.uk/login"

def validate(proxy):
    options = Options()
    options.add_argument('--headless')

    PROXY = proxy

    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
            }


    profile = webdriver.FirefoxProfile()
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',False)
    profile.set_preference("media.peerconnection.enabled", False)

    user_agent = headers.get_user_agent()
    profile.set_preference("general.useragent.override", user_agent)

    with webdriver.Firefox(profile, options=options) as driver:
        try:
            driver.set_page_load_timeout(45)
            driver.get(URL)

            iframe = WebDriverWait(driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, '//iframe[@id="main-iframe"]')))

            driver.switch_to.frame(iframe)

            element = WebDriverWait(driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, '//textarea[@class="g-recaptcha-response"]')))

            with open('valid.txt', 'a') as f:
                f.writelines(f"{proxy}\n")
        except Exception as e:
            print(proxy, ' is not valid')
            raise e


    #driver = webdriver.Firefox(profile, options=options)


""" MULTI PROCESS """
if __name__ == "__main__":

    for start in range(10):
        max_browsers = 20
        end = start * max_browsers if start * max_browsers < len(proxies) else 10
        paginated = proxies[start*max_browsers:end]

        procs = []
        for each in paginated:
            p = mp.Process(target=validate, args=(each,))
            procs.append(p)
            time.sleep(3)
            print('starting browser')
            p.start()
        
        for each in procs:
            each.join()
