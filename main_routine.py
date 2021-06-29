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


def get_next_crawl():
    response = API.fetch_next_crawl()

    if response:
        if response.get('error'):
            logger.info(response['error'])
            return None
        else:
            customer = models.Customer(response.get('customer'))
            proxy = response.get('proxy')

            return (customer, proxy['ip'])
    else:
        logger.info('no response')
        return None

def is_gov_website_working():
    timezone_offset = 1.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    current_time = datetime.now(tzinfo)

    start = datetime.strptime("06:30+0100", "%H:%M%z")
    end = datetime.strptime("23:30+0100", "%H:%M%z")

    if not start.time() < current_time.time() < end.time():
        return False
    elif format(current_time, "%A") == "Sunday":
        return False
    else:
        return True

    #print(f"{current_time.time()} > {start.time()} {current_time.time() > start.time()}")
    #print(f"{current_time.time()} < {end.time()} {current_time.time() < end.time()}")


if __name__ == "__main__":
    while True:
        if not is_gov_website_working():
            time.sleep(600)
            continue

        time.sleep(2)
        crawl_info = get_next_crawl()
        if crawl_info:
            customer, ip = crawl_info
            crawler_instance = DVSACrawler(customer, ip)
            p = mp.Process(target=crawler_instance.scrape)
            p.start()

        
