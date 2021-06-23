import sys
from crawler import DVSACrawler
import logging
from config import logger
import random
import os
import json
from pprint import pprint
#import threading
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
            #data = json.loads(response)
            customer = models.Customer(response.get('customer'))
            proxy = response.get('proxy')

            return (customer, proxy['ip'])

            #c = DVSACrawler(random.choice(proxies))
            #c = DVSACrawler(customer, proxy['ip'])
            #c = DVSACrawler(customer)
            #c.scrape()
    else:
        logger.info('no response')
        return None


if len(sys.argv) >= 2 and sys.argv[1] == 'mp':
    logger.info('RUNNING MANY CRAWLERS')
    #""" MULTI PROCESS """
    if __name__ == "__main__":
        procs = []
        while True:
            time.sleep(5)
            crawl_info = get_next_crawl()
            if crawl_info:
                customer, ip = crawl_info
                crawler_instance = DVSACrawler(customer, ip)
                p = mp.Process(target=crawler_instance.scrape)
                #procs.append(p)
                p.start()
        
            
            #for each in procs:
                #each.join()


else:
    logger.info('RUNNING SINGLE CRAWLER')
    response = API.fetch_next_crawl()
    pprint(response)
    
    if response:
        if response.get('error'):
            logger.info(response['error'])
        else:
            #data = json.loads(response)
    
            customer = models.Customer(response.get('customer'))
            proxy = response.get('proxy')
    
            #c = DVSACrawler(random.choice(proxies))
            c = DVSACrawler(customer, proxy['ip'])
            #c = DVSACrawler(customer)
            c.scrape()
    else:
        logger.info('no response')


