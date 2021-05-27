import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename='var/log/crawler.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

TWOCAPTCHA_API_KEY = os.environ.get('TWOCAPTCHA_API_KEY')
DRIVING_LICENCE_NUMBER = os.environ.get('DRIVING_LICENCE_NUMBER')
TEST_REF = os.environ.get('TEST_REF')
