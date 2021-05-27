import os
from dotenv import load_dotenv

load_dotenv()

TWOCAPTCHA_API_KEY = os.environ.get('TWOCAPTCHA_API_KEY')
DRIVING_LICENCE_NUMBER = os.environ.get('DRIVING_LICENCE_NUMBER')
TEST_REF = os.environ.get('TEST_REF')
