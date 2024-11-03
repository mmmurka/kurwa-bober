from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver import DriverSingleton
from utils.functions import similarity_ratio

varus_link = 'https://varus.ua/search?q='

def search_product_varus(product_name):
    words = product_name.split()
    driver = DriverSingleton.get_driver()

    try:
        while words:
            search_url = varus_link + '%20'.join(words)
            driver.get(search_url)

            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sf-product-card__wrapper'))
                )
            except Exception:
                words.pop()
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='sf-product-card__wrapper')

            if product:
                title = product.find('h2', class_='sf-product-card__title')
                price = product.find('span', class_='sf-price__regular') or product.find('ins', class_='sf-price__special')
                old_price = product.find('del', class_='sf-price__old')

                product_link_tag = product.find('a', class_='sf-link sf-product-card__link')
                link = 'https://varus.ua' + product_link_tag['href'] if product_link_tag else None

                if title and price:
                    title_text = title.text.strip()
                    similarity = similarity_ratio(product_name, title_text)

                    if old_price:
                        return {'price': price.text.strip()[:-3], 'old_price': old_price.text.strip()[:-3], 'match': similarity, 'link': link}
                    else:
                        return {'price': price.text.strip()[:-3], 'match': similarity, 'link': link}
                else:
                    return {'price': '-', 'old_price': '-', 'match': '-', 'link': '-'}
            else:
                words.pop()

            if not words:
                return None
    finally:
        DriverSingleton.quit_driver()
