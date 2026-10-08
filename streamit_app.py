# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# アプリのタイトルと説明文
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order=st.text_input('NAME ON SMOOTHIE')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflakeセッションの取得
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# 複数選択ウィジェット
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# 材料が選択されている場合の処理
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # 送信ボタン
    time_to_submit = st.button('Submit Order')

    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        # 成功メッセージに注文者名を含める
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
