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


#""" MULTI PROCESS """
#if __name__ == "__main__":
#    procs = []
#    for i in range(4):
#        c = DVSACrawler(random.choice(proxies))
#        p = mp.Process(target=c.scrape)
#        procs.append(p)
#        p.start()
#    
#    for each in procs:
#        each.join()


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
