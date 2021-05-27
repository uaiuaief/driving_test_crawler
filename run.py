from crawler import DVSACrawler
import logging

crawler = DVSACrawler() 

#print(crawler.is_customer_info_valid())
print(crawler.scrape())





# Don't forget to close it, or will you have a ton of processes consuming cpu and memory
#crawler.close()

