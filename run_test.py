from datetime import datetime, timezone, timedelta
import sys
from crawler import DVSACrawler
import logging
from config import logger
import random
import os
import json
from pprint import pprint
import multiprocessing as mp
import time
import models
import api_integration as API


user = {
        "id": 72,
        "email": "dvsatestuser@test.com",
        "profile": {
            "first_name": "Test",
            "last_name": "User",
            "mobile_number": None,
            "driving_licence_number": "AHMED952193EO9UK",
            "test_ref": "47350362",
            "theory_test_number": None,
            "test_centers": [
                {
                    "id": 30,
                    "created_at": "2021-07-01T15:36:14.819227+01:00",
                    "last_modified": "2021-07-01T15:36:14.819250+01:00",
                    "name": "Worksop"
                    }
                ],
            "recent_test_failure": None,
            "earliest_test_date": "2021-07-01",
            "latest_test_date": None,
            "earliest_time": "07:00:00",
            "latest_time": "18:00:00",
            "last_crawled": "2021-07-01T15:35:21+01:00",
            "automatic_booking": False,
            "test_booked": False,
            "current_test_date": None,
            "info_validation": "valid"
            }
        }

customer = models.Customer(user)
c = DVSACrawler(customer, "92.242.184.231:3128")
c.scrape()


