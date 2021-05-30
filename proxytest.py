from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import headers




options = Options()
ip = '169.57.157.148'
port = '25'
PROXY = f"{ip}:{port}"
#PROXY = '5.61.58.211:4369'
webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
        }

#options.add_argument(f"--proxy-server{PROXY}")
profile = webdriver.FirefoxProfile()
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',False)
profile.set_preference("media.peerconnection.enabled", False)

user_agent = headers.get_user_agent()
profile.set_preference("general.useragent.override", user_agent)

#with webdriver.Firefox(profile, options=options) as driver:
driver = webdriver.Firefox(profile, options=options)
#driver.get('https://www.whatismyip.com/')
#driver.get('https://www.whatismyip.com/proxy-check/')
#driver.get('https://2ip.io/privacy/')
driver.get('https://thesafety.us/check-ip')
#driver.get('https://proxy6.net/en/privacy')
#driver.get('https://proxy-checker.net/en/privacy/')
