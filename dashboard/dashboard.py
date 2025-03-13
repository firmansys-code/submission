import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

all_df = pd.read_csv("dashboard/main_data.csv")

all_df["dteday"] = pd.to_datetime(all_df["dteday"], errors="coerce").dt.date

st.sidebar.header("⚙️ Pilih Rentang Waktu")
min_date, max_date = all_df["dteday"].min(), all_df["dteday"].max()
start_date, end_date = st.sidebar.date_input("Rentang waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

filtered_df = all_df[(all_df["dteday"] >= start_date) & (all_df["dteday"] <= end_date)]

if not filtered_df.empty:

    weekday_stats = filtered_df.groupby("weekday").agg({"instant": "nunique", "cnt": ["max", "min"]}).reset_index()
    weekday_stats.columns = ["Weekday", "Unique Records", "Max Rentals", "Min Rentals"]

    workingday_stats = filtered_df.groupby("workingday").agg({"instant": "nunique", "cnt": ["max", "min"]}).reset_index()
    workingday_stats.columns = ["Workingday", "Unique Records", "Max Rentals", "Min Rentals"]

    holiday_stats = filtered_df.groupby("holiday").agg({"instant": "nunique", "cnt": ["max", "min"]}).reset_index()
    holiday_stats.columns = ["Holiday", "Unique Records", "Max Rentals", "Min Rentals"]

    weather_stats = filtered_df.groupby("weathersit").agg({"instant": "nunique", "cnt": ["max", "min"]}).reset_index()
    weather_stats.columns = ["Weathersit", "Unique Records", "Max Rentals", "Min Rentals"]

    hourly_stats = filtered_df.groupby("hr").agg({"instant": "nunique", "cnt": ["max", "min"]}).reset_index()
    hourly_stats.columns = ["Hour", "Unique Records", "Max Rentals", "Min Rentals"]

    st.header("📊 Dashboard Statistik Penyewaan Sepeda")
    st.write("📆 **Weekday**")
    st.dataframe(weekday_stats)

    st.write("🏢 **Workingday**")
    st.dataframe(workingday_stats)

    st.write("⛅ Weather")
    st.dataframe(weather_stats)
    
    st.write("🎉 **Holiday**")
    st.dataframe(holiday_stats)

    st.write("⏰ **Hour**")
    st.dataframe(hourly_stats)

    def plot_bar_chart(df, x_col, title, labels):
        fig, ax = plt.subplots(figsize=(8, 5))
        df_melted = df.melt(id_vars=x_col, var_name="Metric", value_name="Value")
        sns.barplot(data=df_melted, x=x_col, y="Value", hue="Metric", palette="coolwarm", ax=ax)

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel(labels["x"])
        ax.set_ylabel(labels["y"])
        plt.xticks(rotation=45)

        st.pyplot(fig)

    plot_bar_chart(weekday_stats, "Weekday", "Penyewaan Berdasarkan Hari ", {"x": "Hari", "y": "Jumlah Penyewaan"})
    plot_bar_chart(workingday_stats, "Workingday", "Penyewaan Berdasarkan Hari Kerja", {"x": "Hari Kerja (0: Libur, 1: Bekerja)", "y": "Jumlah Penyewaan"})
    plot_bar_chart(holiday_stats, "Holiday", "Penyewaan Berdasarkan Hari Libur", {"x": "Hari Libur (0: Tidak Libur, 1: Libur)", "y": "Jumlah Penyewaan"})
    plot_bar_chart(hourly_stats, "Hour", "Penyewaan Berdasarkan Jam", {"x": "Jam (0-23)", "y": "Jumlah Penyewaan"})

    total_users = filtered_df[["casual", "registered"]].sum().reset_index()
    total_users.columns = ["Customer Type", "Total Users"]

    sizes = total_users["Total Users"]
    labels = [f"{cat} ({val:,.0f})" for cat, val in zip(total_users["Customer Type"], total_users["Total Users"])]
    colors = ["skyblue", "salmon"]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'edgecolor': 'black'})
    ax.set_title("Proporsi Penyewa Sepeda Casual vs Registered", fontsize=14, fontweight="bold")

    st.pyplot(fig)

    daily_rentals = filtered_df.groupby("dteday")[["casual", "registered"]].sum().reset_index()
    
    st.subheader("📊 Visualisasi Penyewaan Sepeda Harian")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=daily_rentals.melt(id_vars="dteday", var_name="Tipe", value_name="Jumlah"), 
                x="dteday", y="Jumlah", hue="Tipe", palette="viridis", ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewa Sepeda")
    ax.set_title("Perbandingan Penyewa Sepeda Casual vs Registered")
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    st.dataframe(daily_rentals)

st.caption('Copyright (c) Proyek Analisis Data')
