import asyncio

import pandas as pd

from shop.silpo import search_product_silpo

df = pd.read_excel('prodick.xlsx')

async def write_prices():
    for product in df['Unnamed: 2'].iloc[5:10]:
        silpo_product = await search_product_silpo(product)

        print(silpo_product)


asyncio.run(write_prices())