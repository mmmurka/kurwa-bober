import asyncio
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

from utils.driver import DriverSingleton
from utils.functions import similarity_ratio

makeup_link = 'https://makeup.com.ua/ua/search/?q='


async def search_makeup_product(barcodes):
    codes = str(barcodes).split(',')
    driver = DriverSingleton.get_driver()
    try:
        for code in codes:
            product_link = makeup_link + code
            driver.get(product_link)

            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'simple-slider-list__link'))
                )
            except TimeoutException:
                return {'price': 'Товар не знайдено'}

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='simple-slider-list__link')

            if product:
                out_of_stock = product.find('div', class_='simple-slider-list__price_container').find('span', class_='simple-slider-list__description', string='Немає в наявності')
                if out_of_stock:
                    return {'price': 'Товару немає в наявності'}
                title = product.find('a', class_='simple-slider-list__name')
                price = product.find('span', class_='simple-slider-list__price').find('span', class_='price_item')
                old_price = product.find('span', class_='simple-slider-list__price_old').find('span', class_='price_item')
                link = 'https://makeup.com.ua' + title['href']
                if old_price:
                    return {'price': price.text.strip(), 'old_price': old_price.text.strip(), 'link': link, 'match': 100}
                else:
                    return {'price': price.text.strip(), 'link': link, 'match': 100}

    except Exception as e:
        logging.error(e)
    finally:
        DriverSingleton.quit_driver()

#  del in prod
async def main():
    responce = await search_makeup_product('1278068')

    print(responce)


if __name__ == '__main__':
    asyncio.run(main())
