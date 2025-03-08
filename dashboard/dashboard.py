import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

hour_df = pd.read_csv("dashboard/main_data.csv")

st.title("Analisis Data Penyewaan Sepeda")

st.subheader("Statistik Deskriptif Data Penyewaan Sepeda")
st.dataframe(hour_df.describe())  

weather_rentals = hour_df.groupby(by="weathersit")["cnt"].nunique().sort_values(ascending=False)

st.title("Analisis Penyewaan Sepeda Berdasarkan Cuaca")

st.subheader("Jumlah Unik Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
st.dataframe(weather_rentals)  

#
daily_avg_rentals = hour_df.groupby("mnth")["cnt"].mean().reset_index()
daily_avg_rentals = daily_avg_rentals.rename(columns={"cnt": "avg_rentals_per_day"})

month_labels = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

st.title("Analisis Penyewaan Sepeda per Bulan")

st.subheader("Tabel Rata-rata Penyewaan Sepeda per Hari")
st.dataframe(daily_avg_rentals)  

st.subheader("Visualisasi Rata-rata Penyewaan Sepeda per Hari dalam Setiap Bulan")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="mnth", y="avg_rentals_per_day", data=daily_avg_rentals, hue="mnth", palette="Blues", legend=False, ax=ax)

ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan Sepeda per Hari")
ax.set_title("Rata-rata Penyewaan Sepeda per Hari dalam Setiap Bulan")
ax.set_xticks(range(0, 12))
ax.set_xticklabels(month_labels)

st.pyplot(fig)

monthly_comparison = hour_df.groupby("mnth")[["casual", "registered"]].mean().reset_index()

monthly_comparison_melted = monthly_comparison.melt(id_vars="mnth", var_name="Customer Type", value_name="Avg Rentals Per Day")

month_labels = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

st.title("Analisis Penyewaan Sepeda: Pelanggan Kasual vs Terdaftar")

st.subheader("Tabel Rata-rata Penyewaan Sepeda per Hari Berdasarkan Jenis Pelanggan")
st.dataframe(monthly_comparison_melted)

st.title("Visualisasi Penyewaan Sepeda per Bulan")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="mnth", y="Avg Rentals Per Day", hue="Customer Type", data=monthly_comparison_melted, palette="Set2", ax=ax)

ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan per Hari")
ax.set_title("Rata-rata Penyewaan Sepeda per Hari oleh Pelanggan Kasual vs Pelanggan Tetap")
ax.set_xticks(range(0, 12))
ax.set_xticklabels(month_labels)
ax.legend(title="Tipe Pelanggan")

st.pyplot(fig)
