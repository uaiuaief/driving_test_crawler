from crawler import DVSACrawler
import logging
from proxylist import proxies
import random
import os
#import threading
import multiprocessing as mp
import time


proxies = []
with open('utils/valid.txt', 'r') as f:
    for each in f.readlines():
        proxies.append(each.strip())


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

c = DVSACrawler(random.choice(proxies))
c.scrape()
