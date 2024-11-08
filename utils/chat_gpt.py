import asyncio
import logging

from ChatGPT.chat_api import ChatGPT


a = 'Прокладки Always Platinum Ultra Night 12шт'
b = 'Гігієнічні прокладки Always Platinum Day & Night, розмір 3, 22 шт'

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
            Також виводити matcing percentage

            Вихід:
            Повернути Це різні товари/Це однакові товари у вигляді "однакові/різні - matching precentage" де matching 
            percentage - відсоток співпадінь між назвами, тільки цифра
            
        """)

    logging.info(f"Назва з Excel: {excel}, назва з магазину: {shop}")

    result = await chatGPT.get_response(user_message=f'''
        *працюй по цьому промту(пиши тільки відповідь Це різні товари/Це однакові товари)
            Назва з Excel: {excel}
            Назва з магазину: {shop}
    ''', temperature=0.0)

    logging.info(f'Chat response: {result}')
    print(result)

    return True, result.split('-')[-1] if 'однакові' in result else False


async def main():
    responce = await get_response(a, b)

    print(responce)

if __name__ == '__main__':
    asyncio.run(main())
