import pandas as pd
from shop.eva import search_product_eva
from shop.silpo import search_product_silpo
from shop.varus import search_product_varus
from shop.makeup import search_product_makeup

# Путь к Excel-файлу
file_path = 'hh.xlsx'


def update_excel_with_shop_data():
    df = pd.read_excel(file_path)

    products = df['Unnamed: 2'].iloc[1:-1]
    hashcodes_list = df['Unnamed: 1'].iloc[1:-1]

    for index, (product, hashcodes) in enumerate(zip(products, hashcodes_list), start=1):
        print(f"{index} - Processing product: {product}, hashcodes: {hashcodes}")

        # Поиск и обновление для makeup
        # makeup_product = search_product_makeup(product, hashcodes)
        # if makeup_product:
        #     df.at[index, 'makeup'] = makeup_product.get('price')
        #     df.at[index, 'Unnamed: 12'] = makeup_product.get('old_price') if makeup_product.get(
        #         'old_price') else makeup_product.get('price')
        #     df.at[index, 'Unnamed: 13'] = makeup_product.get('link', '')
        #     df.at[index, 'Unnamed: 14'] = makeup_product.get('match', '')
        #     print(f"Makeup: {makeup_product} внесено")

        varus_product = search_product_varus(product)
        if varus_product:
            df.at[index, 'varus'] = varus_product.get('price')
            df.at[index, 'Unnamed: 16'] = varus_product.get('old_price') if varus_product.get('old_price') else varus_product.get('price')
            df.at[index, 'Unnamed: 17'] = varus_product.get('link', '')
            df.at[index, 'Unnamed: 18'] = varus_product.get('match', '')
            print(f"Varus: {varus_product} внесено")

    df.to_excel(file_path, index=False)
    print("Excel file updated successfully.")


update_excel_with_shop_data()
