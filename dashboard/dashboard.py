import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set agar tampilan dashboard lebar
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Menyiapkan Data
day_df = pd.read_csv("dashboard/main_data.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

# Penyesuaian Nama Kolom & Tipe Data 
date_col = 'date' if 'date' in day_df.columns else 'dteday'
weather_col = 'weather_condition' if 'weather_condition' in day_df.columns else 'weathersit'
cnt_col = 'total_count' if 'total_count' in day_df.columns else 'cnt'

day_df[date_col] = pd.to_datetime(day_df[date_col])
hour_df[date_col] = pd.to_datetime(hour_df[date_col])

# Merubah angka jadi teks di dashboard
if day_df['season'].dtype in ['int64', 'float64']:
    day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
if day_df[weather_col].dtype in ['int64', 'float64']:
    day_df[weather_col] = day_df[weather_col].map({1: 'Cerah', 2: 'Berkabut', 3: 'Hujan/Salju Ringan', 4: 'Cuaca Buruk'})

# SIDEBAR
min_date = day_df[date_col].min()
max_date = day_df[date_col].max()

with st.sidebar:
    st.title("Bike Sharing Filter")
    st.write("Silakan pilih rentang waktu data:")
    
    # Widget kalender untuk filter waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan input dari sidebar
filtered_day_df = day_df[(day_df[date_col] >= pd.to_datetime(start_date)) & 
                         (day_df[date_col] <= pd.to_datetime(end_date))]
filtered_hour_df = hour_df[(hour_df[date_col] >= pd.to_datetime(start_date)) & 
                           (hour_df[date_col] <= pd.to_datetime(end_date))]

# MAIN DASHBOARD
st.title('Bike Sharing Dashboard')
st.markdown(f"**Menampilkan data dari: {start_date} hingga {end_date}**")

# Menampilkan metrik utama
total_sewa = filtered_day_df[cnt_col].sum()
st.metric("Total Penyewaan Sepeda (Pada Rentang Waktu Ini)", value=f"{total_sewa:,}")
st.markdown("---")

# Visualisasi 1 & 2 (Menjawab Pertanyaan 1)
col1, col2 = st.columns(2)

with col1:
    st.subheader('Pengaruh Musim Terhadap Penyewaan')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_season = {'Spring': '#D3D3D3', 'Summer': '#D3D3D3', 'Fall': '#005b96', 'Winter': '#D3D3D3'}
    sns.barplot(x='season', y=cnt_col, data=filtered_day_df, palette=colors_season, order=['Spring', 'Summer', 'Fall', 'Winter'], ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Total Penyewaan')
    st.pyplot(fig)

with col2:
    st.subheader('Pengaruh Cuaca Terhadap Penyewaan')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_weather = {'Cerah': '#005b96', 'Berkabut': '#D3D3D3', 'Hujan/Salju Ringan': '#D3D3D3', 'Cuaca Buruk': '#D3D3D3'}
    # Filter cuaca yang ada di data saat ini biar tidak error
    existing_weather = filtered_day_df[weather_col].dropna().unique()
    order_weather = [w for w in ['Cerah', 'Berkabut', 'Hujan/Salju Ringan', 'Cuaca Buruk'] if w in existing_weather]
    
    sns.barplot(x=weather_col, y=cnt_col, data=filtered_day_df, palette=colors_weather, order=order_weather, ax=ax)
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Total Penyewaan')
    st.pyplot(fig)

# Visualisasi 3: Jam Sibuk (Menjawab Pertanyaan 2)
st.subheader('Tren Jam Sibuk Penyewaan Sepeda: Hari Kerja vs Hari Libur')
fig, ax = plt.subplots(figsize=(12, 6))

filtered_hour_df['Keterangan'] = filtered_hour_df['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

sns.pointplot(
    x='hr', 
    y='cnt' if 'cnt' in filtered_hour_df.columns else cnt_col, 
    hue='Keterangan', 
    data=filtered_hour_df, 
    palette={'Hari Libur': '#ff8c8c', 'Hari Kerja': '#5dade2'}, 
    ax=ax
)
ax.set_xlabel('Jam (00.00 - 23.00)')
ax.set_ylabel('Rata-rata Penyewaan')
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

st.caption('Copyright (c) Lita Rahma Sadina 2026')