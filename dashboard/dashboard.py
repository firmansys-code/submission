import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

all_df = pd.read_csv("dashboard/main_data.csv")

all_df["dteday"] = pd.to_datetime(all_df["dteday"], errors="coerce").dt.date 
st.title("📊 Analisis Data Penyewaan Sepeda")

st.subheader("Statistik deskriptif data penyewaan sepeda")
st.dataframe(all_df.describe())  

weather_stats = all_df.groupby(by="weathersit").agg({
    "instant": "nunique",
    "cnt": ["max", "min", "mean", "std"]
}).reset_index()

weather_stats.columns = ["Weathersit", "Unique Records", "Max Rentals", "Min Rentals", "Avg Rentals", "Std Dev Rentals"]

st.title("📊 Analisis Penyewaan Sepeda Berdasarkan Cuaca")

st.subheader("📋 Statistik Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
st.dataframe(weather_stats)

st.markdown("""
#### Keterangan kondisi cuaca berdasarkan weathersit:
- 1 : cerah, sedikit awan, sebagian berawan.
- 2 : kabut, mendung.
- 3 : salju ringan, hujan ringan.
- 4 : hujan lebat, hujan es, badai petir, salju disertai kabut.
""")

daily_avg_rentals = all_df.groupby("mnth")["cnt"].mean().reset_index()
daily_avg_rentals = daily_avg_rentals.rename(columns={"cnt": "avg_rentals_per_day"})

month_labels = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

st.title("📊 Analisis Penyewaan Sepeda per Hari tiap Bulan")

st.subheader("Tabel rata-rata penyewaan sepeda per hari tiap bulan")
st.dataframe(daily_avg_rentals)

total_users = all_df[["casual", "registered"]].sum().reset_index()
total_users.columns = ["Customer Type", "Total Users"]

# Buat Pie Chart
sizes = total_users["Total Users"]
labels = [f"{cat} ({val:,.0f})" for cat, val in zip(total_users["Customer Type"], total_users["Total Users"])]
colors = ["skyblue", "salmon"]

fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'edgecolor': 'black'})
ax.set_title("Proporsi Penyewa Sepeda Casual vs Registered", fontsize=14, fontweight="bold")

# Tampilkan di Streamlit
st.title("🚲 Total Penyewaan Sepeda Casual vs Registered")
st.pyplot(fig)

st.title("🚲 Analisis Penyewaan Sepeda Casual vs Registered")

st.sidebar.header("⚙️ Pilih rentang waktu untuk menampilkan data penyewaan sepeda casual dan registered")
min_date, max_date = all_df["dteday"].min(), all_df["dteday"].max()
start_date, end_date = st.sidebar.date_input("Rentang waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

filtered_df = all_df[(all_df["dteday"] >= start_date) & (all_df["dteday"] <= end_date)].groupby("dteday")[["casual", "registered"]].sum().reset_index()

if filtered_df.empty:
    st.warning(f"❌ Tidak ada data dalam rentang {start_date} hingga {end_date}. Pilih rentang lain.")
else:
    st.subheader(f"Penyewaan sepeda dari {start_date} hingga {end_date}")
    st.write(filtered_df)

    st.subheader("📊 Visualisasi Penyewaan Sepeda")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=filtered_df.melt(id_vars="dteday", var_name="Tipe", value_name="Jumlah"), x="dteday", y="Jumlah", hue="Tipe", palette="viridis", ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewa Sepeda")
    ax.set_title("Perbandingan Penyewa Sepeda Casual vs Registered")
    plt.xticks(rotation=45)

    st.pyplot(fig)

#
