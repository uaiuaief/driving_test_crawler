import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('crawler')

logging.basicConfig(filename='var/log/crawler.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG, filemode='w')

logger.addHandler(logging.StreamHandler())

TWOCAPTCHA_API_KEY = os.environ.get('TWOCAPTCHA_API_KEY')
DRIVING_LICENCE_NUMBER = os.environ.get('DRIVING_LICENCE_NUMBER')
TEST_REF = os.environ.get('TEST_REF')
