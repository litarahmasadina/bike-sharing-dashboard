import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 1. Menyiapkan Data
day_df = pd.read_csv("dashboard/main_data.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

st.header('Bike Sharing Dashboard')

# Visualisasi 1: Musim 
st.subheader('Rata-rata Penyewaan Sepeda Berdasarkan Musim')
fig1, ax1 = plt.subplots(figsize=(10, 5))
colors_season = ["#D3D3D3", "#D3D3D3", "#005b96", "#D3D3D3"]
sns.barplot(x='season', y='cnt', data=day_df, palette=colors_season, ax=ax1)
st.pyplot(fig1)

# Visualisasi 2: Jam Sibuk
st.subheader('Tren Jam Sibuk: Hari Kerja vs Hari Libur')
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.pointplot(x='hr', y='cnt', hue='workingday', data=hour_df, palette='Set1', ax=ax2)
ax2.set_xlabel('Jam (0-23)')
ax2.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig2)

st.caption('Copyright (c) Lita Rahma Sadina 2026')