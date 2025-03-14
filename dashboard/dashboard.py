import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

main_data_path = "https://raw.githubusercontent.com/YanWed/project_analisa_data/refs/heads/main/dashboard/main_data.csv"  
df = pd.read_csv(main_data_path)
df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
df["season"] = df["month"].map({1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring", 6: "Summer", 
                                   7: "Summer", 8: "Summer", 9: "Autumn", 10: "Autumn", 11: "Autumn", 12: "Winter"})

with st.sidebar:
    location = st.selectbox("Pilih Lokasi:", df['station'].unique())
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=df["datetime"].min().date(), 
        max_value=df["datetime"].max().date(),
        value=[df["datetime"].min().date(), df["datetime"].max().date()]
    )

filtered_df = df[(df["station"] == location) & 
                 (df["datetime"].dt.date >= start_date) & 
                 (df["datetime"].dt.date <= end_date)]

st.header('Dashboard Kualitas Udara')
st.subheader(f'Analisis Data Polusi di {location}')

# Rata-rata Polusi dan Suhu
col1, col2, col3 = st.columns(3)
with col1:
    avg_pm25 = round(filtered_df["PM2.5"].mean(), 2)
    st.metric("Rata-rata PM2.5", value=f"{avg_pm25} µg/m³")
with col2:
    avg_pm10 = round(filtered_df["PM10"].mean(), 2)
    st.metric("Rata-rata PM10", value=f"{avg_pm10} µg/m³")
with col3:
    avg_temp = round(filtered_df["TEMP"].mean(), 2)
    st.metric("Rata-rata Suhu", value=f"{avg_temp}°C")

st.subheader(f"Tren PM2.5 dan PM10 di {location}")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df["datetime"], filtered_df["PM2.5"], label="PM2.5", color="red", marker='o', linestyle='-')
ax.plot(filtered_df["datetime"], filtered_df["PM10"], label="PM10", color="blue", marker='s', linestyle='--')
ax.set_xlabel("Waktu")
ax.set_ylabel("Konsentrasi (µg/m³)")
ax.set_title(f"Perubahan PM2.5 dan PM10 di {location}")
ax.legend()
st.pyplot(fig)

st.subheader("Polusi Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df[df['station'] == location], x="season", y="PM2.5", ax=ax, palette="coolwarm", width=0.6)
sns.boxplot(data=df[df['station'] == location], x="season", y="PM10", ax=ax, palette="Blues", width=0.4)
ax.set_xlabel("Musim")
ax.set_ylabel("Konsentrasi Polusi (µg/m³)")
ax.set_title(f"Distribusi PM2.5 dan PM10 Berdasarkan Musim di {location}")
st.pyplot(fig)

st.subheader(f"Hubungan Faktor Cuaca dengan PM2.5 dan PM10 ({location})")
weather_pollution = filtered_df[["TEMP", "WSPM", "RAIN", "PM2.5", "PM10"]].dropna()
corr_matrix = weather_pollution.corr()
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.caption('Copyright © 2025')
