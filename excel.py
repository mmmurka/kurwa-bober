import pandas as pd
from varus_selenium import search_product_with_selenium

file_path = 'prod.xlsx'
df = pd.read_excel(file_path)
pd.set_option('display.max_colwidth', None)

column_data = df['Unnamed: 2'].tolist()
for name in column_data[1:]:
    search_product_with_selenium(name)


