import requests
import json


url = 'http://localhost:8000/api/add-available-dates/Nott'
payload = {
        'dates': {
            '1-6-2021': [
                '08:05',
                '09:15',
                '09:45',
                ],
            '3-8-2021': [
                '12:00',
                '15:30',
                ]
            }
        }

r = requests.post(url, json=payload)

print(r.status_code)
