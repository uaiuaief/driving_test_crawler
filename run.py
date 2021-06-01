from crawler import DVSACrawler
import logging
from proxylist import proxies
import random
import os
import json
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

if response:
    #data = json.loads(response)

    customer = models.Customer(response.get('customer'))
    proxy = response.get('proxy')

    #c = DVSACrawler(random.choice(proxies))
    c = DVSACrawler(customer, proxy['ip'])
    #c = DVSACrawler(customer)
    c.scrape()

else:
    print('no customer or proxies available')


