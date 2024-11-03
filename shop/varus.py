from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
                # Ожидание загрузки карточек продуктов
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sf-product-card__link'))
                )

                # Извлечение ссылки с помощью selenium
                product_link_tag = driver.find_element(By.CLASS_NAME, 'sf-product-card__link')
                link = product_link_tag.get_attribute('href')

                # Проверка и корректировка ссылки
                if link and not link.startswith('http'):
                    link = 'https://varus.ua' + link

                # Извлечение названия и цены
                title = driver.find_element(By.CLASS_NAME, 'sf-product-card__title').text.strip()
                price = driver.find_element(By.CLASS_NAME, 'sf-price__regular').text.strip().replace(' грн', '')

                # Проверка старой цены
                try:
                    old_price = driver.find_element(By.CLASS_NAME, 'sf-price__old').text.strip().replace(' грн', '')
                except:
                    old_price = None

                # Подсчет схожести
                similarity = similarity_ratio(product_name, title)

                return {
                    'price': price,
                    'old_price': old_price,
                    'match': similarity,
                    'link': link
                }

            except Exception:
                # Если элемент не найден, удаляем последнее слово и продолжаем без вывода ошибок
                words.pop()
                continue

        # Если после всех итераций товар не найден, возвращаем None
        return None

    finally:
        DriverSingleton.quit_driver()
