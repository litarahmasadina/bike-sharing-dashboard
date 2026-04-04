import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")

# Menyiapkan Data
day_df = pd.read_csv("dashboard/main_data.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

st.header('Bike Sharing Dashboard')

# Visualisasi 1 & 2 (Dibuat Berdampingan)
col1, col2 = st.columns(2)

with col1:
    st.subheader('Rata-rata Penyewaan Berdasarkan Musim')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_season = ["#D3D3D3", "#D3D3D3", "#005b96", "#D3D3D3"]
    sns.barplot(x='season', y='cnt', data=day_df, palette=colors_season, ax=ax)
    ax.set_xlabel('Musim (1: Springer, 2: Summer, 3: Fall, 4: Winter)')
    ax.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

with col2:
    st.subheader('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_weather = ["#005b96", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x='weathersit', y='cnt', data=day_df, palette=colors_weather, ax=ax)
    ax.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Mendung, 3: Hujan/Salju Ringan)')
    ax.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig)

# Visualisasi 3: Jam Sibuk
st.subheader('Tren Jam Sibuk Penyewaan Sepeda: Hari Kerja vs Hari Libur')
fig, ax = plt.subplots(figsize=(12, 6))

# Ubah angka 0 & 1 jadi teks biar legendanya bagus
hour_df['Keterangan'] = hour_df['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

sns.pointplot(
    x='hr', 
    y='cnt', 
    hue='Keterangan', 
    data=hour_df, 
    palette={'Hari Libur': '#ff8c8c', 'Hari Kerja': '#5dade2'}, 
    ax=ax
)
ax.set_xlabel('Jam (00.00 - 23.00)')
ax.set_ylabel('Rata-rata Penyewaan')
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

st.caption('Copyright (c) Lita Rahma Sadina 2026')