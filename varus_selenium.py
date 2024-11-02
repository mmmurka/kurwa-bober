from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def search_product_with_selenium(product_name):
    # Настройки для Selenium
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Инициализация драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Открываем страницу с поисковым запросом
        search_url = f"https://varus.ua/search?q={product_name.replace(' ', '%20')}"
        driver.get(search_url)

        # Ждем, чтобы страница полностью загрузилась
        time.sleep(3)  # Лучше использовать WebDriverWait вместо sleep для надежности

        # Находим все товары на странице
        products = driver.find_elements(By.CLASS_NAME, "sf-product-card__block")  # Проверить, подходит ли класс

        if not products:  # Если нет товаров
            print("На жаль, товар не знайдено.")
            return

        # Извлекаем данные о первом товаре
        product = products[0]
        name = product.find_element(By.CLASS_NAME, "sf-product-card__title").text.strip()

        # Извлекаем ссылку на товар
        product_link_elements = product.find_elements(By.CLASS_NAME, "sf-link.sf-product-card__link.sf-product-card__title-wrapper")
        product_link = product_link_elements[0].get_attribute("href") if product_link_elements else None

        # Инициализируем переменные для цен
        old_price = None
        special_price = None

        # Проверяем наличие старой и специальной цены
        old_price_elements = product.find_elements(By.CLASS_NAME, "sf-price__old")
        special_price_elements = product.find_elements(By.CLASS_NAME, "sf-price__special")

        if old_price_elements:
            old_price = old_price_elements[0].text.strip()
        if special_price_elements:
            special_price = special_price_elements[0].text.strip()

        # Если специальной цены нет, проверяем обычную
        if not special_price:
            regular_price_elements = product.find_elements(By.CLASS_NAME, "sf-price__regular")
            special_price = regular_price_elements[0].text.strip() if regular_price_elements else None

        # Определяем, как вывести цену
        if special_price:
            price_output = f"Стара ціна: {old_price}, Ціна зі знижкою: {special_price}" if old_price else f"{special_price}"
        else:
            price_output = "немає в наявності"

        # Выводим информацию о первом товаре
        print(f"Назва товару: {name}")
        print(f"Ціна: {price_output}")
        if product_link:
            print(f"Лінк на товар: {product_link}")

    finally:
        # Закрываем браузер
        driver.quit()


# Пример использования функции
product_name = "Прокладки Kotex Natural Нічні 6шт"
search_product_with_selenium(product_name)
