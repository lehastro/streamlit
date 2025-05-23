import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Случайные числа", layout="centered")

st.title("📊 Таблица из 100 случайных чисел")

# Генерация 100 случайных чисел
data = pd.DataFrame({
    "Число": np.random.randint(0, 1000, size=100)
})

# Отображение таблицы
st.dataframe(data)
