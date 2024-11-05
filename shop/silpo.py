import asyncio
import logging

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from utils.chat_gpt import get_response
from utils.driver import DriverSingleton

silpo_link = 'https://silpo.ua/search?find='

async def search_silpo_product(name):
    driver = DriverSingleton.get_driver()
    product_link = silpo_link + '%20'.join(name.split())
    driver.get(product_link)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'products-list__item'))
        )
    except TimeoutException:
        return {'price': 'Товар не знайдено'}
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.find_all('div', class_='products-list__item ng-star-inserted')
        if products:
            for product in products:
                title = product.find('div', class_='product-card__title')
                gpt_info = await get_response(name, title)
                if gpt_info[0] is True:
                    if product.find('div', data_autotestid_='cart-soldout'):
                        return {'price': 'Товару немає в наявності', 'match': gpt_info[1]}
                    price = product.find('div', class_='ft-text-22')
                    old_price = product.find('div', class_='ft-line-through')
                    product_link_tag = product.find('a', class_='product-card')
                    link = 'https://silpo.ua/' + product_link_tag['href'] if product_link_tag else None
                    if old_price:
                        return {'price': price.text.strip()[:-3], 'old_price': old_price.text.strip()[:-3], 'link': link, 'match': gpt_info[1]}
                    else:
                        return {'price': price.text.strip()[:-3], 'link': link, 'match': gpt_info[1]}
    except Exception as e:
        logging.error(e)
    finally:
        DriverSingleton.quit_driver()


#  delete on prod
async def main():
    responce = await search_silpo_product('Рол з тунцем та хіяши')

    print(responce)


if __name__ == '__main__':
    asyncio.run(main())
