import datetime
import requests
from pprint import pprint
from config import logger, CRAWLER_USERNAME, CRAWLER_PASSWORD

URL = 'https://www.quickdrivingtest.co.uk/api'
#URL = 'http://localhost:8000/api'
CREDENTIALS = (CRAWLER_USERNAME, CRAWLER_PASSWORD)


def validate_customer_info(customer_pk):
    _set_customer_info(customer_pk, 'valid')

def invalidate_customer_info(customer_pk):
    _set_customer_info(customer_pk, 'invalid')

def _set_customer_info(customer_pk, value):
    endpoint = f"set-user-info-validation"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.post(
            full_url, 
            auth=CREDENTIALS,
            json={
        'user_id': customer_pk,
        'info_validation': value
        })

    r.raise_for_status()

def set_customer_current_test_date(customer_pk, date_time):
    endpoint = f"set-current-test-date"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')

    #Format = 01-01-2021 15:00
    formatted_date = format(date_time, "%d-%m-%Y %H:%M")

    r = requests.post(
            full_url, 
            auth=CREDENTIALS,
            json={
        'user_id': customer_pk,
        'datetime': formatted_date
        })

    r.raise_for_status()

def set_test_booked(customer_pk):
    endpoint = f"set-test-booked"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')

    r = requests.post(
            full_url, 
            auth=CREDENTIALS,
            json={
        'user_id': customer_pk,
        })

    r.raise_for_status()

def ban_proxy(ip):
    endpoint = f"ban-proxy"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.post(
            full_url, 
            auth=CREDENTIALS,
            json={
                'ip': ip,
            })

    r.raise_for_status()

def fetch_next_crawl():
    endpoint = f"proxy-customer-pair"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.get(full_url, auth=CREDENTIALS)
    r.raise_for_status()

    if r.status_code == 200:
        return r.json()
    else: 
        return None

def send_test_found_email(data):
    endpoint = f"test-found"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')

    r = requests.post(
            full_url, 
            auth=CREDENTIALS,
            json={
                'user_id': data['user_id'],
                'test_time': data['test_time'],
                'test_date': data['test_date'],
                'test_center_id': data['test_center_id'],
            })
    #pprint(r.json())
    r.raise_for_status()

    if r.status_code == 200:
        return r.json()
    else: 
        return None

def fetch_unchecked_users():
    endpoint = f"unchecked-customers"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.get(full_url, auth=CREDENTIALS)
    r.raise_for_status()

    if r.status_code == 200:
        return r.json()
    else: 
        return None

def fetch_valid_proxy():
    endpoint = f"valid-proxy"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')
    r = requests.get(full_url, auth=CREDENTIALS)
    r.raise_for_status()

    if r.status_code == 200:
        return r.json()
    else: 
        return None

def send_info_invalid_email(data):
    endpoint = f"test-found"
    full_url = f"{URL}/{endpoint}/"
    logger.debug(f'fetching: {full_url}')

    r = requests.post(
            full_url, 
            auth=CREDENTIALS,
            json={
                'user_id': data['user_id'],
                'test_time': data['test_time'],
                'test_date': data['test_date'],
                'test_center_id': data['test_center_id'],
            })
    #pprint(r.json())
    r.raise_for_status()

    if r.status_code == 200:
        return r.json()
    else: 
        return None

if __name__ == "__main__":
    data = {
            'user_id': 1,
            'test_time': format(datetime.datetime.now(), "%H:%M"),
            'test_date': format(datetime.datetime.now(), "%d-%m-%y"),
            'test_center_id': 2,
            }


    #dt = datetime.datetime.now()
    #set_test_booked(66)

