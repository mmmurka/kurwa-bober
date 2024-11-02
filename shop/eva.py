from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils.driver import DriverSingleton
from utils.functions import similarity_ratio

eva_link = 'https://eva.ua/ua/search/?q='


def search_product_eva(product_name):
    driver = DriverSingleton.get_driver()
    words = product_name.split()
    try:
        while words:
            product_link = eva_link + '%20'.join(words)
            driver.get(product_link)

            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'product__details'))
                )
            except Exception:
                words.pop()
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='product__details')

            if product:
                title = product.find('span', {'aria-label': True})

                price = product.find('span', class_='product__special-price')
                old_price = product.find('span', class_='product__regular-price')

                product_link_tag = product.find('a', class_='product__link')
                link = 'https://eva.ua' + product_link_tag['href'] if product_link_tag else None

                if title and price:
                    title_text = title['aria-label'].strip()
                    similarity = similarity_ratio(product_name, title_text)

                    if old_price:
                        return {'price': price.text.strip()[:-3], 'old_price': old_price.text.strip()[:-3],
                                'match': similarity, 'link': link}
                    else:
                        return {'price': price.text.strip()[:-3], 'match': similarity, 'link': link}
                else:
                    words.pop()

                if not words:
                    return None
    finally:
        DriverSingleton.quit_driver()