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


if __name__ == "__main__":
    while True:
        time.sleep(5)
        crawl_info = get_next_crawl()
        if crawl_info:
            customer, ip = crawl_info
            crawler_instance = DVSACrawler(customer, ip)
            p = mp.Process(target=crawler_instance.scrape)
            p.start()
        
