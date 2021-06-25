import time
import schedule
from config import logger
import models
from crawler import DVSACrawler
import api_integration as api


def job():
    data = api.fetch_unchecked_users()

    if not data:
        logger.info('no data')
        return

    users = data.get('customers')

    if not users:
        return

    user = users[0]
    data = api.fetch_valid_proxy()

    if not data:
        return

    proxy = api.fetch_valid_proxy().get('proxy')

    if not proxy:
        logger.info('no proxy avaliable')
        return

    logger.info(f'checking user {user.get("email")}')
    customer = models.Customer(user)
    crawler = DVSACrawler(customer, proxy.get('ip'))
    info_valid = crawler.is_customer_info_valid()

    if info_valid == True:
        api.validate_customer_info(customer.id)
    elif info_valid == False:
        api.invalidate_customer_info(customer.id)

        
job()

schedule.every(1).minutes.do(job)


while True:
    time.sleep(2)
    schedule.run_pending()

