import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

#Title
st.title('Welcome To Rent Bike Dashboard')

#Load data day.csv
day_df= pd.read_csv('day.csv')

#Load data hour.csv
hour_df = pd.read_csv('hour.csv')

#Menampilkan Dataset day_df
st.header("Data Frame Bike Rented by Day")
st.dataframe(day_df, height=400)

#Menampilkan Dataset hour_df
st.header("Data Frame Bike Rented by Hour")
st.dataframe(hour_df, height=400)

#Build a column
col1,col2=st.columns(2)

#Menunjukkan Jumlah Hari Total
with col1:
    counts=day_df.instant.count()
    st.metric("Total Days: ", value=counts)
#Menunjukkan Jumlah Jam Total
with col2 :
    counts_hours=hour_df.instant.count()
    st.metric("Total Hours :", value=counts_hours)

#Pertanyaan 1
st.header('Pertanyaan 1')
st.header('Bagaimana persebaran peminjaman sepeda perharinya?')

#Menunjukkan visualisasi data untuk pertanyaan 1
fig, ax= plt.subplots(figsize=(10,6))

sns.boxplot(
    y="cnt",
    x="weekday",
    data=day_df,
    palette="viridis")


day_label=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
plt.xticks(ticks=range(len(day_label)), labels=day_label)
plt.title("Bike Rented By Days", loc="center", fontsize=15)
plt.xlabel("Days")
plt.tick_params(axis="x", labelsize=12)
plt.ylabel("Rented Bike")
st.pyplot(fig)

#Set Caption untuk visualisasi data 1
st.caption('Boxplot Persebaran Peminjaman Sepeda Per Hari')

#Set penjelasan untuk visualisasi data 1
with st.expander("Penjelasan Grafik"):
    st.write(
        """*   Distribusi penyewaan sepeda yang beragam setiap harinya
*   Penyewaan tertinggi berada pada hari Jumat
*   Hari Rabu memiliki median yang lebih rendah
*   Tingkat penyewaan lebih tinggi pada akhir pekan terlihat dari angka median yang lebih tinggi
"""
)

#Pertanyaan 2
st.header('Pertanyaan 2')
st.header(' Bagaimana pola peminjaman sepeda dengan berdasarkan pengaruh waktu (perjam)?')

#Menyimpan jumlah peminjaman berdasarkan jam 
hour_count_df = hour_df.groupby(by="hr")["cnt"].sum().reset_index()

#Menunjukkan visualisasi data untuk pertanyaan 2
fig, ax= plt.subplots(figsize=(10,6))

sns.lineplot(
    y="cnt",
    x="hr",
    data=hour_count_df,
    legend=False
)
sns.scatterplot(
    y="cnt",
    x="hr",
    data=hour_count_df,
    color='green',
    s=100,
    ax=ax
)

hour_label=list(range(0,24))
plt.xticks(ticks=range(len(hour_label)), labels=hour_label)
plt.title("Bike Rented By Hours", loc="center", fontsize=15)
plt.xlabel("Hours")
plt.tick_params(axis="x", labelsize=12)
plt.ylabel("Rented Bike")

st.pyplot(fig)
#Set caption visualisasi data 2
st.caption('Line Chart Total Peminjaman Sepeda Per Jam')

#Set penjelasan visualisasi data 2
with st.expander("Penjelasan Grafik"):
    st.write(
        """*   Grafik dibuat berdasarkan jumlah total penyewaan sepeda yang terjadi setiap jamnya
*   Puncak pertama pada gragfik jumlah penyewaan sepeda terjadi pada jam 08.00
*   Jumlah penyewaan tertinggi keseluruhan terjadi pada jam 17.00
*   Jumlah penyewaan terendah terjadi pada jam 04.00
*   Persebaran penyewaaan sepeda berdasarkan jam cukup fluktuatif
"""
)
    
#Analisis Lanjutan
st.header('Analisis Lanjutan')
st.header('Pengelompokkan Level Temprature')

# Grafik Temprature per hari
fig, ax= plt.subplots(figsize=(10,6))
sns.lineplot(x=day_df['dteday'], y=day_df['temp'])
plt.title('Temprature per day')
plt.xlabel('Date')
plt.ylabel('Temprature')

st.pyplot(fig)

#Didefinisikan range level temprature low, medium dan high
bins=[0,0.3,0.6,1]
labels=['Low', 'Medium', 'High']

#Pengelompokan berdasarkan range level temprature yang telah ditentukan
day_df['temp_range']=pd.cut(day_df['temp'], bins=bins, labels=labels)

#Menghitung jumlah berdasarkan level temprature yang telah didapatkan
temp_counts = day_df['temp_range'].value_counts()

#Visualisasi Data Grafik jumlah peminjaman berdasarkan level temprature
fig, ax= plt.subplots(figsize=(10,6))
sns.barplot(x=temp_counts.index, y=temp_counts.values)
plt.title('Temperature Level Count')
plt.xlabel('Temperature Level')
plt.ylabel('Count')
st. pyplot(fig)

#Set Caption visualisasi data analisis lanjutan
st.caption("Jumlah Peminjaman Sepeda Berdasarkan Kategori Level Temprature")

#Set penjelasan visualisasi data analisis lanjutan
with st.expander("Penjelasan Grafik"):
    st.write(
        """Dibuat pengelompokkan berdasarkan tempratur yang akan dibagi menjadi 3 range yaitu low, medium, dan high dengan range yang didefinisikan :
- Low = 0-0.3
- Medium = 0.3-0.6
- High = 0.6-1

Insight yang didapat :
*   Grafik menunjukkan bahwa jumlah peminjaman sepeda terbanyak terjadi pada kategori suhu Medium.
*   Peminjaman sepeda pada suhu Low paling sedikit, sementara suhu High memiliki jumlah peminjaman yang berada di tengah-tengah.
"""
)

