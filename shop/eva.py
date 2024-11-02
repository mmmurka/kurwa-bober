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
    found_product = False
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
                        print(
                            f"Назва: {title_text}, Ціна зі знижкою: {price.text.strip()}, Стара ціна: {old_price.text.strip()}, Відсоток співпадіння: {similarity}%", link)
                        print('-' * 100)
                    else:
                        print(f"Назва: {title_text}, Ціна: {price.text.strip()}, Відсоток співпадіння: {similarity}%", link)
                        print('-' * 100)
                    found_product = True
                else:
                    print("Назва або ціна не знайдені")
                    print('-' * 100)
            else:
                words.pop()

            if not words:
                print(f"Товар '{product_name}' не знайдено після всіх спроб.")
                print('-' * 100)

            if found_product:
                break
    finally:
        DriverSingleton.quit_driver()
