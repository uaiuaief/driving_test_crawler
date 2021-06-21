import requests
from pprint import pprint
from config import logger

URL = 'http://localhost:8000/api'

def validate_customer_info(customer_pk):
    _set_customer_info(customer_pk, 'valid')

def invalidate_customer_info(customer_pk):
    _set_customer_info(customer_pk, 'invalid')

def _set_customer_info(customer_pk, value):
    endpoint = f"set-user-info-validation"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.post(full_url, json={
        'user_id': customer_pk,
        'info_validation': value
        })
    r.raise_for_status()

def ban_proxy(ip):
    endpoint = f"ban-proxy"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.post(full_url, json={
        'ip': ip,
        })
    r.raise_for_status()

def fetch_next_crawl():
    endpoint = f"proxy-customer-pair"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.get(full_url)
    #r.raise_for_status()

    if r.status_code == 200:
        return r.json()
    else: 
        return None

