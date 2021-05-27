import requests

URL = 'http://localhost:8000/api'

def validate_customer_info(customer_pk):
    endpoint = f"customers"
    full_url = f"{URL}/{endpoint}/{customer_pk}/"
    print(full_url)
    r = requests.patch(full_url, json={'info_validation':'valid'})
    r.raise_for_status()

def invalidate_customer_info(customer_pk):
    endpoint = f"customers"
    full_url = f"{URL}/{endpoint}/{customer_pk}/"
    print(full_url)
    r = requests.patch(full_url, json={'info_validation':'invalid'})
    r.raise_for_status()

def add_dates(test_center, dates):
    endpoint = f"add-available-dates"
    full_url = f"{URL}/{endpoint}/{test_center}/"
    r = requests.post(full_url, json=dates)
    print(r.text)
    r.raise_for_status()


