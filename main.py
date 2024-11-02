import pandas as pd
from shop.eva import search_product_eva
from shop.silpo import search_product_silpo
from shop.varus import search_product_varus
from shop.makeup import search_product_makeup


df = pd.read_excel('/Users/mmmurka/PycharmProjects/piskya-parser/prod.xlsx')

search_product_eva('Засіб Lactacyd для інтимної гігієни 200мл')
search_product_silpo('Засіб Lactacyd для інтимної гігієни 200мл')
search_product_varus('Засіб Lactacyd для інтимної гігієни 200мл')
for original_name, hashcodes in zip(df['Unnamed: 2'].iloc[1:-1], df['Unnamed: 1'].iloc[1:-1]):
    search_product_makeup(original_name, hashcodes)
