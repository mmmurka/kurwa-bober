import asyncio

from ChatGPT.chat_api import ChatGPT

excel_name = 'Підгузки Tena для дорослих Pants Normal 30p'
user = 'Підгузки-трусики Tena Pants Medium+, 30шт'


async def get_response(excel: str, shop: str):
    chatGPT = ChatGPT(
        role=f"""
    Завдання: Порівняти дві назви товарів і визначити, чи це один товар чи різні. Ігнорувати стоп-слова.

Вхідні дані:
- Назва з Excel: {excel}
- Назва з магазину: {shop}

Процедура:
1. Очистити назви від стоп-слів.
2. Привести обидві назви до нижнього регістру.
3. Порівняти назви, враховуючи можливі синоніми, варіації, переклади ключових слів з англійської на українську (наприклад, "Night" і "ніч" трактувати як одне й те саме слово).
4. Ігнорувати символи типу "+" і "Plus", вважаючи їх еквівалентними.
5. Використати метрику схожості, що дозволяє врахувати відмінності в порядку слів та незначні відмінності у формулюваннях.

Вихід:
- Вивести це один і той самий товар, або це різні товари.
""")
    result = await chatGPT.get_response()
    return result


async def main():
    result = await get_response(excel_name, user)
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
