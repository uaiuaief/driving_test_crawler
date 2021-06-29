import datetime
import unittest
from pprint import pprint
from models import Customer, TestCenter


class TestCustomerModel(unittest.TestCase):
    customer = None
    data = None

    def setUp(self):
        self.data = {
                "id": 66,
                "email": "laura.c.shepherd@gmail.com",
                "profile": {
                    "first_name": "Laura",
                    "last_name": "Shepherd",
                    "mobile_number": "07984498933",
                    "driving_licence_number": "SHEPH956017LC9HJ",
                    "test_ref": "45670645",
                    "theory_test_number": 'null',
                    "test_centers": [
                        {
                            "id": 18,
                            "name": "West Didsbury (Manchester)"
                            }
                        ],
                    "recent_test_failure": "2021-06-28",
                    "earliest_test_date": "2021-06-29",
                    "latest_test_date": "2021-07-31",
                    "earliest_time": "10:00:00",
                    "latest_time": "15:00:00",
                    "automatic_booking": False,
                    "test_booked": False,
                    "current_test_date": 'null',
                    "info_validation": "valid"
                    }
        }

        self.customer = Customer(self.data)

    def test_customer_has_all_keys(self):
        keys = [
                'id',
                'driving_licence_number',
                'test_ref',
                'test_centers',
                'recent_test_failure',
                'earliest_test_date',
                'latest_test_date',
                'earliest_time',
                'latest_time',
                'info_validation',
                'automatic_booking',
                'test_booked',
                'current_test_date',
        ]

        for k in keys:
            self.assertTrue(hasattr(self.customer, k))

    def test_test_centers(self):
        self.assertIs(type(self.customer.test_centers), list)

    def test_empty_test_centers(self):
        self.data['profile']['test_centers'] = None
        with self.assertRaises(ValueError):
            customer = Customer(self.data)

    def test_earliest_test_date(self):
        self.assertIs(type(self.customer.earliest_test_date), datetime.date)

    def test_latest_test_date(self):
        self.assertIs(type(self.customer.latest_test_date), datetime.date)

    def test_earliest_time(self):
        self.assertIs(type(self.customer.earliest_time), datetime.time)

    def test_latest_time(self):
        self.assertIs(type(self.customer.latest_time), datetime.time)


