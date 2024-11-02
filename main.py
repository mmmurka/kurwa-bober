import pandas as pd
from shop.eva import search_product_eva
from shop.silpo import search_product_silpo
from shop.varus import search_product_varus
from shop.makeup import search_product_makeup


# df = pd.read_excel('/Users/mmmurka/PycharmProjects/piskya-parser/prod.xlsx')
#
# search_product_eva('Засіб Lactacyd для інтимної гігієни 200мл')
# print(search_product_silpo('Засіб Lactacyd для інтимної гігієни 200мл'))
# search_product_varus('Засіб Lactacyd для інтимної гігієни 200мл')
# for original_name, hashcodes in zip(df['Unnamed: 2'].iloc[1:-1], df['Unnamed: 1'].iloc[1:-1]):
#     search_product_makeup(original_name, hashcodes)

# Path to the prod.xlsx file
file_path = 'hh.xlsx'

def update_excel_with_shop_data():
    df = pd.read_excel(file_path)

    products = [product for product in df['Unnamed: 2'].iloc[1:5]]
    hashcodes = [hashcode for hashcode in df['Unnamed: 1'].iloc[1:-1]]

    for index, product in enumerate(products, start=1):
        varus_product = search_product_varus(product)
        # silpo_product = search_product_silpo(product)
        # makeup_product = search_product_makeup(product, hashcodes)
        # eva_product = search_product_eva(product)
        #
        # if silpo_product:
        #     df.at[index, 'silpo'] = silpo_product.get('price')
        #     df.at[index, 'Unnamed: 8'] = silpo_product.get('old_price') if silpo_product.get('old_price') is not None else silpo_product.get('price')
        #     df.at[index, 'Unnamed: 9'] = silpo_product.get('link', '')
        #     df.at[index, 'Unnamed: 10'] = silpo_product.get('match', '')
        #     print(f"Silpo: {silpo_product} внесено")
        #
        # if eva_product:
        #     df.at[index, 'eva'] = eva_product.get('price')
        #     df.at[index, 'Unnamed: 4'] = eva_product.get('old_price') if eva_product.get('old_price') is not None else eva_product.get('price')
        #     df.at[index, 'Unnamed: 5'] = eva_product.get('link', '')
        #     df.at[index, 'Unnamed: 6'] = eva_product.get('match', '')
        #     print(f"EVA: {eva_product} внесено")
        #
        # if makeup_product:
        #     df.at[index, 'makeup'] = makeup_product.get('price')
        #     df.at[index, 'Unnamed: 12'] = makeup_product.get('old_price') if makeup_product.get('old_price') is not None else makeup_product.get('price')
        #     df.at[index, 'Unnamed: 13'] = makeup_product.get('link', '')
        #     df.at[index, 'Unnamed: 14'] = makeup_product.get('match', '')
        #     print(f"Makeup: {makeup_product} внесено")
        if varus_product:
            df.at[index, 'varus'] = varus_product.get('price')
            df.at[index, 'Unnamed: 16'] = varus_product.get('old_price') if varus_product.get('old_price') is not None else varus_product.get('price')
            df.at[index, 'Unnamed: 17'] = varus_product.get('link', '')
            df.at[index, 'Unnamed: 18'] = varus_product.get('match', '')
            print(f"Varus: {varus_product} внесено")

    df.to_excel(file_path, index=False)

    print("Excel file updated successfully.")

update_excel_with_shop_data()
