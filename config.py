import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('crawler')

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(message)s', '%m/%d/%Y %H:%M:%S')
stream.setFormatter(formatter)

logger.addHandler(stream)

logging.basicConfig(filename='var/log/crawler.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)

#logger.addHandler(logging.StreamHandler())

TWOCAPTCHA_API_KEY = os.environ.get('TWOCAPTCHA_API_KEY')
DRIVING_LICENCE_NUMBER = os.environ.get('DRIVING_LICENCE_NUMBER')
TEST_REF = os.environ.get('TEST_REF')

CRAWLER_USERNAME = os.environ.get('CRAWLER_USERNAME')
CRAWLER_PASSWORD = os.environ.get('CRAWLER_PASSWORD')
