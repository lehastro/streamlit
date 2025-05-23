import streamlit as st
import random

st.set_page_config(page_title="Генератор чисел", layout="centered")

st.title("🎲 Генератор случайных чисел в диапазоне")

# Ввод диапазона
st.markdown("#### Укажите диапазон:")
col1, col2 = st.columns(2)
with col1:
    start = st.number_input("От", value=1, step=1)
with col2:
    end = st.number_input("До", value=100, step=1)

# Кол-во чисел
count = st.number_input("Сколько чисел сгенерировать", value=100, min_value=1, step=1)

# Без повторов
unique = st.checkbox("Без повторов")

# Кнопка
if st.button("Сгенерировать"):
    if end < start:
        st.error("Ошибка: 'До' должно быть больше или равно 'От'")
    else:
        possible_values = end - start + 1
        if unique and count > possible_values:
            st.error(f"Невозможно выбрать {count} уникальных чисел из диапазона {possible_values}")
        else:
            if unique:
                numbers = random.sample(range(start, end + 1), count)
            else:
                numbers = [random.randint(start, end) for _ in range(count)]

            st.subheader("Результат:")
            st.code(", ".join(map(str, numbers)), language="text")
