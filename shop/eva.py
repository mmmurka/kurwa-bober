import asyncio
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

from utils.chat_gpt import get_response
from utils.driver import DriverSingleton
from utils.functions import similarity_ratio

eva_link = 'https://eva.ua/ua/search/?q='


async def search_product_eva(product_name):
    driver = DriverSingleton.get_driver()
    product_link = eva_link + '%20'.join(product_name.split())
    words = product_name.split()
    try:
        driver.get(product_link)

        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product__details'))
            )
        except TimeoutException:
            logging.warning(f"Product {product_name} not found")
            return {'price': 'Товар не знайдено'}

        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='product__details')

            if product:
                title = product.find('span', {'aria-label': True})

                gpt_info = await get_response(product_name, title)
                logging.info(f'Chat response: {gpt_info}')
                if gpt_info[0]:
                    out_of_stock = product.find('div', class_='product__out-of-stock-text')
                    if out_of_stock:
                        logging.info(f"Product {product_name} out of stock")
                        return {'price': 'Товару немає в наявності', 'match': gpt_info[1]}

                    price = product.find('span', class_='product__special-price')
                    old_price = product.find('span', class_='product__regular-price')
                    print(price)

                    product_link_tag = product.find('a', class_='product__link')
                    link = 'https://eva.ua' + product_link_tag['href'] if product_link_tag else None

                    if old_price:
                        return {'price': price.text.strip()[:-3], 'old_price': old_price.text.strip()[:-3],
                                'link': link, 'match': gpt_info[1]}
                    else:
                        return {'price': price.text.strip()[:-3], 'link': link, 'match': gpt_info[1]}

        except Exception as e:
            logging.error(e)

    finally:
        DriverSingleton.quit_driver()

asyncio.run(search_product_eva('Уцінка! Щоденні гігієнічні прокладки Discreet Deo Waterlilly Plus, 52 шт'))
