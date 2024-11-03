from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from utils.driver import DriverSingleton
from utils.functions import similarity_ratio

makeup_link = 'https://makeup.com.ua/ua/search/?q='


def link_creator(shop_link, code):
    return shop_link + str(code)


def search_product_makeup(original_name, hashcodes):
    codes = str(hashcodes).split(',')
    driver = DriverSingleton.get_driver()
    try:
        for code in codes:
            product_link = link_creator(makeup_link, code.strip())
            driver.get(product_link)

            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'simple-slider-list__link'))
                )
            except Exception:
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='simple-slider-list__link')

            if product:
                title = product.find('a', class_='simple-slider-list__name')
                price = product.find('span', class_='price_item')
                old_price = product.find('span', class_='simple-slider-list__price_old .price_item')
                out_of_stock = product.find('div', class_='simple-slider-list__description', string='Немає в наявності')

                if title and 'href' in title.attrs:
                    link = 'https://makeup.com.ua' + title['href']
                else:
                    link = None
                if out_of_stock:
                    return {
                        'message': f"Продукт за штрихкодом {code.strip()} - '{title.text.strip()}' - Немає в наявності",
                        'link': link}
                elif title and price:
                    title_text = title.text.strip()
                    similarity = similarity_ratio(original_name, title_text)
                    if old_price:
                        return {'price': price.text.strip(), 'old_price': old_price.text.strip(), 'link': link,
                                'match': similarity}
                    else:
                        return {'price': price.text.strip(), 'link': link, 'match': similarity}

        similarity = 0
        link = 'product not found'
        price = '-'
        return {'price': price, 'link': link, 'match': similarity}
    finally:
        DriverSingleton.quit_driver()
