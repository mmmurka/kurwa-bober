import asyncio
import logging

from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver import DriverSingleton

from utils.chat_gpt import get_response


varus_link = 'https://varus.ua/search?q='


async def search_product_varus(product_name):
    print(product_name)
    driver = DriverSingleton.get_driver()
    search_url = varus_link + '%20'.join(product_name.split())
    try:
        driver.get(search_url)

        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'sf-product-card__wrapper'))
            )
        except TimeoutException:
            logging.warning(f"Product {product_name} not found")
            return {'price': 'Товар не знайдено'}

        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='sf-product-card__wrapper')

            if product:
                title = product.find('h2', class_='sf-product-card__title')

                gpt_info = await get_response(product_name, title)
                logging.info(f'Chat response: {gpt_info}')

                if gpt_info[0]:
                    out_of_stock = product.find('div', class_='sf-product-card__out-of-stock')
                    if out_of_stock:
                        logging.info(f"Product {product_name} out of stock")
                        return {'price': 'Товару немає в наявності', 'match': gpt_info[1]}

                    price = product.find('span', class_='sf-price__regular') or product.find('ins', class_='sf-price__special')
                    old_price = product.find('del', class_='sf-price__old')

                    product_link_tag = product.find('a', class_='sf-link sf-product-card__link')
                    link = 'https://varus.ua' + product_link_tag['href'] if product_link_tag else None

                    if old_price:
                        return {'price': price.text.strip()[:-3], 'old_price': old_price.text.strip()[:-3],
                                'link': link, 'match': gpt_info[1]}
                    else:
                        return {'price': price.text.strip()[:-3], 'link': link, 'match': gpt_info[1]}
        except Exception as e:
            logging.error(e)
    finally:
        DriverSingleton.quit_driver()

asyncio.run(search_product_varus('Засіб Lactacyd для інтимної гігієни з дозатором 200 мл'))
