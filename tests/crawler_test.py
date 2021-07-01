import datetime
import unittest
from pprint import pprint
from models import Customer, TestCenter
from crawler import DVSACrawler


class TestCrawler(unittest.TestCase):
    customer = None
    data = None
    crawler = None

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
                    "current_test_date": "2021-11-03T08:10:00Z",
                    "info_validation": "valid"
                    }
        }

        self.customer = Customer(self.data)
        self.crawler = DVSACrawler(self.customer)

    #@unittest.skip("testing other")
    def test_to_military_time(self):
        minutes = [str(i).zfill(2) for i in range(60)]
        hours_twelve = [str(i+1).zfill(2) for i in range(12)]

        ampm_times = []
        for h in hours_twelve:
            for m in minutes:
                ampm_times.append(f"{h}:{m}am")
        for h in hours_twelve:
            for m in minutes:
                ampm_times.append(f"{h}:{m}pm")

        hours_twenty_four = [str(i+1).zfill(2) for i in range(23)]
        hours_twenty_four.append('00')

        military_times = []
        for h in hours_twenty_four:
            if h == '12':
                h = '00'
            elif h == '00':
                h = '12'
            for m in minutes:
                    military_times.append(f"{h}:{m}")

        for current, expected in zip(ampm_times, military_times):
            result = self.crawler.to_military_time(current)
            self.assertEqual(result, expected)

    #@unittest.skip("testing other")
    def test_is_before_current_test_date(self):
        #date before time before = True
        result = self.crawler.is_before_current_test_date("2021-11-02", "08:09")
        self.assertTrue(result)

        #date before time after = True
        result = self.crawler.is_before_current_test_date("2021-11-02", "08:11")
        self.assertTrue(result)
        
        #date before time equal = True
        result = self.crawler.is_before_current_test_date("2021-11-02", "08:10")
        self.assertTrue(result)

        #date equal time before = True
        result = self.crawler.is_before_current_test_date("2021-11-03", "08:09")
        self.assertTrue(result)

        #date equal time equal = False
        result = self.crawler.is_before_current_test_date("2021-11-03", "08:10")
        self.assertFalse(result)

        #date equal time after = False
        result = self.crawler.is_before_current_test_date("2021-11-03", "08:11")
        self.assertFalse(result)

        #date after time before = False
        result = self.crawler.is_before_current_test_date("2021-11-04", "08:09")
        self.assertFalse(result)

        #date after time equal = False
        result = self.crawler.is_before_current_test_date("2021-11-04", "08:10")
        self.assertFalse(result)
        
        #date after time after = False
        result = self.crawler.is_before_current_test_date("2021-11-04", "08:11")
        self.assertFalse(result)
        
        with self.assertRaises(TypeError):
            self.crawler.is_before_current_test_date(None, "08:10")
            self.crawler.is_before_current_test_date("2021-11-04", None)
            self.crawler.is_before_current_test_date(123123, "08:10")

        with self.assertRaises(ValueError):
            self.crawler.is_before_current_test_date("2021/11/04", "08:10")
            self.crawler.is_before_current_test_date("2021-11-04", "08:10:00")

    #@unittest.skip("testing other")
    def test_is_day_within_customer_date_range(self):
        date_found = "2021-06-28"
        result = self.crawler.is_day_within_customer_date_range(date_found)
        self.assertFalse(result)
        
        date_found = "2021-06-29"
        result = self.crawler.is_day_within_customer_date_range(date_found)
        self.assertTrue(result)

        date_found = "2021-07-10"
        result = self.crawler.is_day_within_customer_date_range(date_found)
        self.assertTrue(result)
        
        date_found = "2021-07-31"
        result = self.crawler.is_day_within_customer_date_range(date_found)
        self.assertTrue(result)

        date_found = "2021-08-01"
        result = self.crawler.is_day_within_customer_date_range(date_found)
        self.assertFalse(result)

    #@unittest.skip("testing other")
    def test_is_day_within_refundable_range(self):
        date_today = datetime.datetime.today().date()

        date_found = format(date_today, "%Y-%m-%d")
        result = self.crawler.is_day_within_refundable_range(date_found)
        self.assertFalse(result)

        date_found = format(date_today + datetime.timedelta(days=1), "%Y-%m-%d")
        result = self.crawler.is_day_within_refundable_range(date_found)
        self.assertFalse(result)

        date_found = format(date_today + datetime.timedelta(days=2), "%Y-%m-%d")
        result = self.crawler.is_day_within_refundable_range(date_found)
        self.assertFalse(result)

        date_found = format(date_today + datetime.timedelta(days=3), "%Y-%m-%d")
        result = self.crawler.is_day_within_refundable_range(date_found)
        self.assertFalse(result)

        date_found = format(date_today + datetime.timedelta(days=4), "%Y-%m-%d")
        result = self.crawler.is_day_within_refundable_range(date_found)
        self.assertFalse(result)

        date_found = format(date_today + datetime.timedelta(days=5), "%Y-%m-%d")
        result = self.crawler.is_day_within_refundable_range(date_found)
        self.assertTrue(result)

        date_found = format(date_today + datetime.timedelta(days=6), "%Y-%m-%d")
        result = self.crawler.is_day_within_refundable_range(date_found)
        self.assertTrue(result)

    #@unittest.skip("testing other")
    def test_is_day_after_recent_failure_date_limit(self):
        date_found = "2021-06-12"
        recent_test_failure = self.customer.recent_test_failure
        result = self.crawler.is_day_after_recent_failure_date_limit(date_found)
        self.assertFalse(result)

        date_found = "2021-07-12"
        recent_test_failure = self.customer.recent_test_failure
        result = self.crawler.is_day_after_recent_failure_date_limit(date_found)
        self.assertFalse(result)

        date_found = "2021-07-13"
        recent_test_failure = self.customer.recent_test_failure
        result = self.crawler.is_day_after_recent_failure_date_limit(date_found)
        self.assertFalse(result)

        date_found = "2021-07-14"
        recent_test_failure = self.customer.recent_test_failure
        result = self.crawler.is_day_after_recent_failure_date_limit(date_found)
        self.assertTrue(result)

        date_found = "2021-07-15"
        recent_test_failure = self.customer.recent_test_failure
        result = self.crawler.is_day_after_recent_failure_date_limit(date_found)
        self.assertTrue(result)

        date_found = "2021-07-16"
        recent_test_failure = self.customer.recent_test_failure
        result = self.crawler.is_day_after_recent_failure_date_limit(date_found)
        self.assertTrue(result)

        date_found = "2021-08-30"
        recent_test_failure = self.customer.recent_test_failure
        result = self.crawler.is_day_after_recent_failure_date_limit(date_found)
        self.assertTrue(result)

        self.crawler.customer.recent_test_failure = None
        result = self.crawler.is_day_after_recent_failure_date_limit("2021-06-29")
        self.assertTrue(result)

    #@unittest.skip("testing other")
    def test_is_time_within_range(self):
        time_found = "09:59"
        result = self.crawler.is_time_within_range(time_found)
        self.assertFalse(result)

        time_found = "10:00"
        result = self.crawler.is_time_within_range(time_found)
        self.assertTrue(result)

        time_found = "14:59"
        result = self.crawler.is_time_within_range(time_found)
        self.assertTrue(result)

        time_found = "15:00"
        result = self.crawler.is_time_within_range(time_found)
        self.assertTrue(result)

        time_found = "15:01"
        result = self.crawler.is_time_within_range(time_found)
        self.assertFalse(result)

    def test_can_test_be_booked(self):
        date_found = "2021-06-28"
        time_found = "10:00"

        result = self.crawler.can_test_be_booked(date_found, time_found)
        self.assertFalse(result)

        date_found = "2021-07-20"
        time_found = "11:00"
        result = self.crawler.can_test_be_booked(date_found, time_found)
        self.assertTrue(result)

