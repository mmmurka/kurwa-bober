import asyncio

import pandas as pd

from shop.silpo import search_silpo_product

df = pd.read_excel('prodick.xlsx')

async def write_prices():
    for product in df['Unnamed: 2'].iloc[5:10]:
        silpo_product = await search_silpo_product(product)

        print(silpo_product)


asyncio.run(write_prices())