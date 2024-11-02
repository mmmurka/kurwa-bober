from utils.functions import similarity_ratio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils.driver import DriverSingleton


silpo_link = 'https://silpo.ua/search?find='


def search_product_silpo(name):
    words = name.split()
    found_product = False
    driver = DriverSingleton.get_driver()

    try:
        while words:
            product_link = silpo_link + '%20'.join(words)
            driver.get(product_link)

            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'products-list__item'))
                )
            except Exception:
                words.pop()
                continue

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product = soup.find('div', class_='products-list__item ng-star-inserted')

            if product:
                title = product.find('div', class_='product-card__title')
                price = product.find('div', class_='ft-text-22')
                old_price = product.find('div', class_='ft-line-through')

                product_link_tag = product.find('a', class_='product-card')
                link = 'https://silpo.ua/' + product_link_tag['href'] if product_link_tag else None

                if title and price:
                    title_text = title.text.strip()
                    similarity = similarity_ratio(name, title_text)

                    if old_price:
                        print(
                            f"Назва: {title_text}, Ціна зі знижкою: {price.text.strip()}, Стара ціна: {old_price.text.strip()}, Відсоток співпадіння: {similarity}%", {link})
                        print('-' * 100)
                    else:
                        print(f"Назва: {title_text}, Ціна: {price.text.strip()}, Відсоток співпадіння: {similarity}%", {link})
                        print('-' * 100)
                    found_product = True
                else:
                    print("Назва або ціна не знайдені")
                    print('-' * 100)
            else:
                words.pop()

            if not words:
                print(f"Товар '{name}' не знайдено після всіх спроб.")
                print('-' * 100)

            if found_product:
                break
    finally:
        DriverSingleton.quit_driver()


