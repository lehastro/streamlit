import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Storage Calculator", layout="wide")
st.title("💾 Расчёт объёмов хранения цифровых слайдов")

st.sidebar.header("Параметры")

slides_per_day = st.sidebar.number_input("Количество слайдов в день", value=977, min_value=1)
slide_size_gb = st.sidebar.number_input("Средний размер 1 слайда (ГБ)", value=1.5, min_value=0.1, step=0.1)
formats_count = st.sidebar.number_input("Количество форматов конвертации", value=2, min_value=1)
converter_speed = st.sidebar.number_input("Производительность одного конвертера (слайдов в день)", value=192, min_value=1)

storage_policies = {
    "Политика 1 (10 лет)": {
        "share": 0.9,
        "retention_days": 3650,
    },
    "Политика 2 (5 лет)": {
        "share": 0.05,
        "retention_days": 1825,
    },
    "Политика 3 (1 год)": {
        "share": 0.05,
        "retention_days": 365,
    },
}

max_years = 10
daily_volume_gb = slides_per_day * slide_size_gb * formats_count

# Объём по годам с учётом ретеншна
data = []
total_storage_by_year = np.zeros(max_years)
for policy, conf in storage_policies.items():
    share = conf["share"]
    retention = conf["retention_days"]
    daily_share_gb = daily_volume_gb * share
    for year in range(1, max_years + 1):
        days_alive = min(retention, year * 365)
        total = daily_share_gb * days_alive
        total_storage_by_year[year - 1] += total
        data.append({
            "Год": year,
            "Политика": policy,
            "Объём (ГБ)": total,
        })

# Таблица
st.subheader("📊 Расчёт объёма хранения по годам")
df = pd.DataFrame(data)
df_pivot = df.pivot(index="Год", columns="Политика", values="Объём (ГБ)")
df_pivot["Итого (ГБ)"] = total_storage_by_year
st.dataframe(df_pivot.style.format("{:.0f}"), use_container_width=True)

# График
st.subheader("📈 Общий объём холодного хранения по годам")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(1, max_years + 1), total_storage_by_year, marker='o')
ax.set_xlabel("Год")
ax.set_ylabel("Объём (ГБ)")
ax.grid(True)
st.pyplot(fig)

# Конвертеры
st.subheader("⚙️ Конвертация")
converters_needed = np.ceil(slides_per_day / converter_speed)
st.markdown(f"Необходимо **{int(converters_needed)}** конвертеров при {converter_speed} слайдах/день на один")
