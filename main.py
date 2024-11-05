import logging

import pandas as pd

from shop.eva import search_product_eva
from shop.silpo import search_product_silpo
from shop.varus import search_product_varus
from shop.makeup import search_product_makeup

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

file_path = 'prod.xlsx'


def update_excel_with_shop_data():
    df = pd.read_excel(file_path)

    products = df['Unnamed: 2'].iloc[1:2]
    hashcodes_list = df['Unnamed: 1'].iloc[1:2]

    for index, (product, hashcodes) in enumerate(zip(products, hashcodes_list), start=1):
        print(product, hashcodes)

        makeup_product = search_product_makeup(product, hashcodes)
        if makeup_product:
            df.at[index, 'makeup'] = makeup_product.get('price')
            df.at[index, 'Unnamed: 12'] = makeup_product.get('old_price') if makeup_product.get(
                'old_price') else makeup_product.get('price')
            df.at[index, 'Unnamed: 13'] = makeup_product.get('link', '')
            df.at[index, 'Unnamed: 14'] = makeup_product.get('match', '')
            print(f"Makeup: {makeup_product} внесено")
        print(product)

        varus_product = search_product_varus(product)
        if varus_product:
            df.at[index, 'varus'] = varus_product.get('price')
            df.at[index, 'Unnamed: 16'] = varus_product.get('old_price') if varus_product.get('old_price') else varus_product.get('price')
            df.at[index, 'Unnamed: 17'] = varus_product.get('link', '')
            df.at[index, 'Unnamed: 18'] = varus_product.get('match', '')
            print(f"Varus: {varus_product} внесено")

        silpo_product = search_product_silpo(product)
        if silpo_product:
            df.at[index, 'silpo'] = silpo_product.get('price')
            df.at[index, 'Unnamed: 8'] = silpo_product.get('old_price') if silpo_product.get('old_price') else silpo_product.get('price')
            df.at[index, 'Unnamed: 9'] = silpo_product.get('link', '')
            df.at[index, 'Unnamed: 10'] = silpo_product.get('match', '')
            print(f"Silpo: {silpo_product} внесено")

        eva_product = search_product_eva(product)
        if eva_product:
            df.at[index, 'eva'] = eva_product.get('price')
            df.at[index, 'Unnamed: 24'] = eva_product.get('old_price') if eva_product.get('old_price') else eva_product.get('price')
            df.at[index, 'Unnamed: 25'] = eva_product.get('link', '')
            df.at[index, 'Unnamed: 26'] = eva_product.get('match', '')
            print(f"Eva: {eva_product} внесено")

    df.to_excel(file_path, index=False)
    print("Excel file updated successfully.")


update_excel_with_shop_data()
