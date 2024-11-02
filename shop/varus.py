from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.functions import similarity_ratio
from utils.driver import DriverSingleton


def search_product_varus(product_name):
    driver = DriverSingleton.get_driver()
    try:
        search_url = f"https://varus.ua/search?q={product_name.replace(' ', '%20')}"
        driver.get(search_url)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sf-product-card__block"))
        )

        products = driver.find_elements(By.CLASS_NAME, "sf-product-card__block")

        if not products:
            print("На жаль, товар не знайдено.")
            print('-' * 100)
            return

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
            price_output = f"Стара ціна: {old_price}, Ціна зі знижкою: {special_price}"\
                if old_price else f"{special_price}"
        else:
            price_output = "немає в наявності"

        match_percentage = similarity_ratio(product_name, name)

        print(f"Назва товару: {name}")
        print(f"Ціна: {price_output}")
        if product_link:
            print(f"Лінк на товар: {product_link}")
        print(f"Відсоток співпадіння: {match_percentage}%")
        print('-' * 100)

        return {'price': special_price, 'old_price': old_price, 'link': product_link, 'match': match_percentage}

    finally:
        DriverSingleton.quit_driver()
