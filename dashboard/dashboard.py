import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')
  
df = pd.read_csv('https://raw.githubusercontent.com/YanWed/project_analisa_data/refs/heads/main/dashboard/main_data.csv')
df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df['season'] = df['datetime'].dt.month.apply(get_season)

df_seasonal = df.groupby('season')[['PM2.5', 'PM10']].mean()

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

st.subheader("Pola Musiman PM2.5 dan PM10")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=df_seasonal.reset_index(), x='season', y='PM2.5', label='PM2.5', alpha=0.7)
sns.barplot(data=df_seasonal.reset_index(), x='season', y='PM10', label='PM10', alpha=0.7)
ax.set_xlabel("Musim")
ax.set_ylabel("Konsentrasi (µg/m³)")
ax.set_title("Pola Musiman PM2.5 dan PM10")
ax.legend()
st.pyplot(fig)

st.subheader("Distribusi PM2.5 dan PM10 Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df[df['station'] == location], x="season", y="PM2.5", hue="station")
ax.set_title("Distribusi PM2.5 Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)")
ax.legend(title="Lokasi")
ax.grid(True)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df[df['station'] == location], x="season", y="PM10", hue="station")
ax.set_title("Distribusi PM10 Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Konsentrasi PM10 (µg/m³)")
ax.legend(title="Lokasi")
ax.grid(True)
st.pyplot(fig)

st.subheader(f"Hubungan Faktor Cuaca dengan PM2.5 dan PM10 ({location})")
weather_pollution = filtered_df[["TEMP", "WSPM", "RAIN", "PM2.5", "PM10"]].dropna()
corr_matrix = weather_pollution.corr()
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.caption('Copyright © 2025')
