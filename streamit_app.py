import requests
import streamlit as st
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake セッションの取得
cnx = st.connection("snowflake")
session = cnx.session()

# FRUIT_NAME と SEARCH_ON の両方のカラムを取得
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# 検索処理を容易にするため Pandas DataFrame に変換
pd_df = my_dataframe.to_pandas()

# 選択肢の表示には FRUIT_NAME を使用
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # 選択された FRUIT_NAME に対応する SEARCH_ON（API用検索キーワード）を取得
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # API リクエストには search_on の値を使用
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to
