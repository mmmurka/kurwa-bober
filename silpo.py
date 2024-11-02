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

silpo_link = 'https://silpo.ua/search?find='

# Зчитування файлу Excel
df = pd.read_excel('h.xlsx')

def similarity_ratio(original, found):
    return round(SequenceMatcher(None, original, found).ratio() * 100, 2)

# Ітерація по товарам із файлу
for name in df['Unnamed: 1'].iloc[1:-1]:
    words = name.split()
    found_product = False

    while words:
        product_link = silpo_link + '%20'.join(words)
        driver.get(product_link)

        # Збільшуємо час очікування для завантаження контенту
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'products-list__item'))
            )
        except Exception:
            words.pop()  # Видаляємо останнє слово, тільки якщо продукт не знайдено
            continue

        # Отримуємо HTML-код сторінки
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product = soup.find('div', class_='products-list__item ng-star-inserted')

        # Перевіряємо, чи знайдений продукт
        if product:
            title = product.find('div', class_='product-card__title')
            price = product.find('div', class_='ft-text-22')
            old_price = product.find('div', class_='ft-line-through')
            discount = product.find('div', class_='product-card-price__sale')
            out_of_stock = product.find('div', class_='cart-soldout', string='Товар закінчився')

            if out_of_stock:
                print(f"Продукт за запитом '{name}' - '{title.text.strip()}' - Товар закінчився")
            elif title and price:
                title_text = title.text.strip()
                similarity = similarity_ratio(name, title_text)

                if old_price and discount:
                    print(
                        f"Назва: {title_text}, Ціна зі знижкою: {price.text.strip()}, Стара ціна: {old_price.text.strip()}, Знижка: {discount.text.strip()}, Відсоток співпадіння: {similarity}%")
                else:
                    print(f"Назва: {title_text}, Ціна: {price.text.strip()}, Відсоток співпадіння: {similarity}%")
                found_product = True
            else:
                print("Назва або ціна не знайдені")
        else:
            words.pop()  # Видаляємо останнє слово, тільки якщо продукт не знайдено

        # Якщо залишилося одне слово і товар не знайдено
        if not words:
            print(f"Товар '{name}' не знайдено після всіх спроб.")

        if found_product:
            break

driver.quit()
