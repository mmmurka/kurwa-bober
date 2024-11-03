from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils.functions import similarity_ratio
from utils.driver import DriverSingleton

varus_link = 'https://varus.ua/search?q='

def search_product_varus(product_name):
    driver = DriverSingleton.get_driver()
    words = product_name.split()
    try:
        while words:
            search_url = varus_link + '%20'.join(words)
            driver.get(search_url)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sf-product-card__block'))
                )
            except Exception:
                words.pop()
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='sf-product-card__block')

            if product:
                title = product.find('a', class_='sf-product-card__title')
                price = product.find('span', class_='sf-price__special')
                old_price = product.find('span', class_='sf-price__old')

                product_link_tag = product.find('a', class_='sf-link.sf-product-card__link.sf-product-card__title-wrapper')
                link = product_link_tag['href'] if product_link_tag else None

                if title and price:
                    title_text = title.text.strip()
                    similarity = similarity_ratio(product_name, title_text)

                    if old_price:
                        return {
                            'price': price.text.strip()[:-3],
                            'old_price': old_price.text.strip()[:-3],
                            'match': similarity,
                            'link': link
                        }
                    else:
                        return {
                            'price': price.text.strip()[:-3],
                            'match': similarity,
                            'link': link
                        }
                else:
                    words.pop()

                if not words:
                    return None
    finally:
        DriverSingleton.quit_driver()
