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
    found_product = False
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

                # Находим тег ссылки и парсим href
                if title and 'href' in title.attrs:
                    link = 'https://makeup.com.ua' + title['href']
                else:
                    link = None
                if out_of_stock:
                    print(f"Продукт за штрихкодом {code.strip()} - '{title.text.strip()}' - Немає в наявності", link)
                elif title and price:
                    title_text = title.text.strip()
                    similarity = similarity_ratio(original_name, title_text)
                    if old_price:
                        print(
                            f"Назва: {title_text}, Нова ціна: {price.text.strip()} грн, Стара ціна: {old_price.text.strip()} грн, Відсоток співпадіння: {similarity}%", link)
                        print('-' * 100)
                    else:
                        print(f"Назва: {title_text}, Ціна: {price.text.strip()} грн, Відсоток співпадіння: {similarity}%",
                              {link})
                        print('-' * 100)
                    found_product = True
                    break
                else:
                    print(f"Назва або ціна не знайдені для штрихкоду {code.strip()}")
                    print('-' * 100)

        if not found_product:
            print(f"Продукт за штрихкодами {codes} не знайдено")
            print('-' * 100)
    finally:
        DriverSingleton.quit_driver()



