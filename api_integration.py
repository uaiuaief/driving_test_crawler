import requests

URL = 'http://localhost:8000/api'

def validate_customer_info(customer_pk):
    endpoint = f"{URL}/customers"
    url = f"{endpoint}/{customer_pk}/"
    print(url)
    r = requests.patch(url, json={'info_validation':'valid'})
    return r

def invalidate_customer_info(customer_pk):
    endpoint = f"{URL}/customers"
    url = f"{endpoint}/{customer_pk}/"
    print(url)
    r = requests.patch(url, json={'info_validation':'invalid'})
    return r
