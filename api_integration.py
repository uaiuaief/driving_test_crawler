import requests
from pprint import pprint
from config import logger

URL = 'http://localhost:8000/api'

def validate_customer_info(customer_pk):
    endpoint = f"customers"
    full_url = f"{URL}/{endpoint}/{customer_pk}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.patch(full_url, json={'info_validation':'valid'})
    r.raise_for_status()

def invalidate_customer_info(customer_pk):
    endpoint = f"customers"
    full_url = f"{URL}/{endpoint}/{customer_pk}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.patch(full_url, json={'info_validation':'invalid'})
    r.raise_for_status()

def add_dates(test_center, dates):
    endpoint = f"add-available-dates"
    full_url = f"{URL}/{endpoint}/{test_center}/"
    r = requests.post(full_url, json=dates)
    logger.info(r.text)
    r.raise_for_status()

def fetch_customer(customer_pk):
    endpoint = f"customers"
    full_url = f"{URL}/{endpoint}/{customer_pk}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.get(full_url)
    print(r.json())

def fetch_next_crawl():
    endpoint = f"proxy-customer-pair"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.get(full_url)
    r.raise_for_status()

    if r.status_code == 200:
        return r.json()
    else: 
        return None




