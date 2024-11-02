from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Підключення до драйвера Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

makeup_link = 'https://makeup.com.ua/ua/search/?q='

# Зчитування файлу Excel
df = pd.read_excel('h.xlsx')


def link_creator(shop_link, code):
    return shop_link + str(code)


def similarity_ratio(original, found):
    return round(SequenceMatcher(None, original, found).ratio() * 100, 2)


# Ітерація по штрихкодам із файлу
for original_name, hashcodes in zip(df['Unnamed: 2'].iloc[1:-1], df['Unnamed: 1'].iloc[1:-1]):
    codes = str(hashcodes).split(',')  # Розділяємо штрихкоди, якщо їх кілька
    found_product = False

    for code in codes:
        product_link = link_creator(makeup_link, code.strip())
        driver.get(product_link)

        # Збільшуємо час очікування для завантаження контенту
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'simple-slider-list__link'))
            )
        except Exception:
            continue

        # Отримуємо HTML-код сторінки
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product = soup.find('div', class_='simple-slider-list__link')

        # Перевіряємо, чи знайдений продукт
        if product:
            title = product.find('a', class_='simple-slider-list__name')
            price = product.find('span', class_='price_item')
            old_price = product.find('span', class_='old-price')  # Додано для пошуку старої ціни
            out_of_stock = product.find('div', class_='simple-slider-list__description', string='Немає в наявності')

            if out_of_stock:
                print(f"Продукт за штрихкодом {code.strip()} - '{title.text.strip()}' - Немає в наявності")
            elif title and price:
                title_text = title.text.strip()
                similarity = similarity_ratio(original_name, title_text)
                if old_price:
                    print(
                        f"Назва: {title_text}, Нова ціна: {price.text.strip()} грн, Стара ціна: {old_price.text.strip()} грн, Відсоток співпадіння: {similarity}%")
                else:
                    print(f"Назва: {title_text}, Ціна: {price.text.strip()} грн, Відсоток співпадіння: {similarity}%")
                found_product = True
                break  # Зупиняємо цикл, якщо знайдено товар
            else:
                print(f"Назва або ціна не знайдені для штрихкоду {code.strip()}")

        # Якщо товар знайдено, зупиняємо пошук
        if found_product:
            break

        else:
            print(f"Продукт за штрихкодом {codes} не знайдено")

driver.quit()
