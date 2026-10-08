import pandas as pd
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# 画面タイトルと説明の表示
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# 注文者名の入力ボックス
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake セッションの取得
cnx = st.connection("snowflake")
session = cnx.session()

# FRUIT_NAME と SEARCH_ON カラムを取得
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))

# 検索キー（SEARCH_ON）を参照しやすくするため Pandas DataFrame に変換
pd_df = my_dataframe.to_pandas()

# トッピング選択マルチセレクト (最大5つ)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# フルーツが1つ以上選択された場合の処理
if ingredients_list:
    ingredients_string = ""

    # 選択されたフルーツごとにループ処理
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "
        
        # FRUIT_NAME に対応する SEARCH_ON の値（API用キーワード）を取得
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        # フルーツ別の栄養情報を API から取得して表示
        st.subheader(fruit_chosen + " Nutrition Information")
        
        # FRUIT_NAME ではなく search_on を使って API を呼び出し
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Snowflake 注文テーブルへの INSERT SQL 文作成
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # 注文送信ボタン
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!", icon="✅")
