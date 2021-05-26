from crawler import DVSACrawler

crawler = DVSACrawler() 
print(crawler.is_customer_info_valid())





# Don't forget to close it, or will you have a ton of processes consuming cpu and memory
#crawler.close()

