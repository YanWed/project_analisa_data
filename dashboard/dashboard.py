import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

main_data_path = r"C:\Users\Asus\Desktop\submission\dashboard\main_data.csv"  
df = pd.read_csv(main_data_path)
df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])

min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()

with st.sidebar:
    location = st.selectbox("Pilih Lokasi:", df['station'].unique())

    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date, 
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_df = df[(df["station"] == location) & 
                 (df["datetime"].dt.date >= start_date) & 
                 (df["datetime"].dt.date <= end_date)]

st.header('Dashboard Kualitas Udara :sparkles:')
st.subheader(f'Analisis Data Polusi di {location}')

col1, col2 = st.columns(2)

with col1:
    avg_pm25 = round(filtered_df["PM2.5"].mean(), 2)
    st.metric("Rata-rata PM2.5", value=f"{avg_pm25} µg/m³")

with col2:
    avg_temp = round(filtered_df["TEMP"].mean(), 2)
    st.metric("Rata-rata Suhu", value=f"{avg_temp}°C")

st.subheader(f"Tren PM2.5 di {location}")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df["datetime"], filtered_df["PM2.5"], label="PM2.5", color="red", marker='o', linestyle='-')
ax.set_xlabel("Waktu")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_title(f"Perubahan PM2.5 di {location}")
ax.legend()
st.pyplot(fig)

st.subheader(f"Korelasi Cuaca vs Polusi ({location})")

weather_pollution = filtered_df[["TEMP", "WSPM", "RAIN", "PM2.5"]].dropna()
corr_matrix = weather_pollution.corr()

fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.caption('Copyright © 2024')