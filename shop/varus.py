from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.functions import similarity_ratio
from utils.driver import DriverSingleton
import math


def search_product_varus(product_name):
    driver = DriverSingleton.get_driver()

    # Проверка, является ли product_name строкой и не NaN
    if not isinstance(product_name, str) or isinstance(product_name, float) and math.isnan(product_name):
        print(f"Невалидное имя товара: {product_name}")
        return {'price': '-', 'link': 'invalid product name', 'match': 0}

    try:
        search_url = f"https://varus.ua/search?q={product_name.replace(' ', '%20')}"
        driver.get(search_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sf-product-card__block"))
            )
        except TimeoutException:
            print(f"Товар '{product_name}' не найден на Varus.")
            return {'price': '-', 'link': 'product not found', 'match': 0}

        products = driver.find_elements(By.CLASS_NAME, "sf-product-card__block")

        if not products:
            print(f"На жаль, товар '{product_name}' не знайдено.")
            return {'price': '-', 'link': 'product not found', 'match': 0}

        product = products[0]
        name = product.find_element(By.CLASS_NAME, "sf-product-card__title").text.strip()

        product_link_elements = product.find_elements(By.CLASS_NAME,
                                                      "sf-link.sf-product-card__link.sf-product-card__title-wrapper")
        product_link = product_link_elements[0].get_attribute("href") if product_link_elements else None

        old_price = None
        special_price = None

        old_price_elements = product.find_elements(By.CLASS_NAME, "sf-price__old")
        special_price_elements = product.find_elements(By.CLASS_NAME, "sf-price__special")

        if old_price_elements:
            old_price = old_price_elements[0].text.strip()
        if special_price_elements:
            special_price = special_price_elements[0].text.strip()

        if not special_price:
            regular_price_elements = product.find_elements(By.CLASS_NAME, "sf-price__regular")
            special_price = regular_price_elements[0].text.strip() if regular_price_elements else None

        if special_price:
            price_output = f"Стара ціна: {old_price}, Ціна зі знижкою: {special_price}" if old_price else f"{special_price}"
        else:
            price_output = "немає в наявності"

        match_percentage = similarity_ratio(product_name, name)

        print(f"Назва товару: {name}")
        print(f"Ціна: {price_output}")
        if product_link:
            print(f"Лінк на товар: {product_link}")
            return {'price': price_output, 'link': product_link, 'match': match_percentage}
        print(f"Відсоток співпадіння: {match_percentage}%")

    finally:
        DriverSingleton.quit_driver()
