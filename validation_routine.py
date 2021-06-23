import time
import schedule
from config import logger
import models
from crawler import DVSACrawler
import api_integration as api


def job():
    data = api.fetch_unchecked_users()
    users = data.get('customers')

    if not users:
        return

    user = users[0]
    proxy = api.fetch_valid_proxy().get('proxy')

    if not proxy:
        logger.info('no proxy avaliable')
        return

    logger.info(f'checking user {user.get("email")}')
    customer = models.Customer(user)
    crawler = DVSACrawler(customer, proxy.get('ip'))
    info_valid = crawler.is_customer_info_valid()
    print(info_valid)

    if info_valid == True:
        api.validate_customer_info(customer.id)
    else:
        api.invalidate_customer_info(customer.id)

        

    

job()
#schedule.every(5).seconds.do(job)
#
#while True:
#    schedule.run_pending()
#    time.sleep(1)

    



