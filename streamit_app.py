import requests
import streamlit as st
from snowflake.snowpark.functions import col

# 画面タイトルと説明の表示
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# 注文者名の入力ボックス
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake セッションの取得 (st.connection を使用)
cnx = st.connection("snowflake")
session = cnx.session()

# フルーツ一覧テーブルから FRUIT_NAME カラムを取得
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

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
        
        # フルーツ別の栄養情報を API から取得して表示
        st.subheader(fruit_chosen + " Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Snowflake 注文テーブルへの INSERT SQL 文作成
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # 注文送信ボタン
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!", icon="✅")
