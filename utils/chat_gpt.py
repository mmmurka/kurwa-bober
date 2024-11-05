import asyncio
import logging

from ChatGPT.chat_api import ChatGPT


a = 'Засіб Lactacyd Свіжість для інтимної гігієни 200мл'
b = 'Засіб для інтимної гігієни Lactacyd «Свіжість» з дозатором, 200мл'

async def get_response(excel: str, shop: str):
    chatGPT = ChatGPT(
        role=f"""
            Завдання: Порівняти дві назви товарів і визначити, чи це один і той самий товар, чи різні.
            Ігнорувати стоп-слова.
            (зайві слова, що не змінюють суть товару, такі як 'для', 'від' тощо).
             
             Увага! - Розглядай "+" як важливу позначку, яка може вказувати на іншу версію товару.

            Вхідні дані:
            Назва з Excel: [Назва товару]
            Назва з магазину: [Назва товару] 

            Процедура:
            1. Видалити стоп-слова з обох назв.
            2. Перевести обидві назви в нижній регістр.
            3. Звернути особливу увагу на важливі характеристики, такі як:
               - Бренд
               - Розмір або формат (наприклад, "Normal", "Medium", "Large", "30 шт")
               - Переклади слів з англійської на українську
               - Специфікації чи позначення (як "+", "Plus", "Pro" тощо)
               - Кількість штук в упаковці та інші показники
            4. Врахувати, що різні позначення можуть вказувати на інший товар, навіть якщо назви схожі.

            Вихід:
            Повернути Це різні товари/Це однакові товари.
            
        """)

    logging.info(f"Назва з Excel: {excel}, назва з магазину: {shop}")

    result = await chatGPT.get_response(user_message=f'''
        *працюй по цьому промту(пиши тільки відповідь Це різні товари/Це однакові товари)
            Назва з Excel: {excel}
            Назва з магазину: {shop}
    ''', temperature=0.0)

    logging.info("Відповідь: %s", result)

    return True if 'однакові' in result else False


async def main():
    responce = await get_response(a, b)

    print(responce)

if __name__ == '__main__':
    asyncio.run(main())
