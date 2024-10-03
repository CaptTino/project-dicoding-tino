import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Data
path_to_file1 = os.path.join(os.path.dirname(__file__), '../Data/day.csv')
path_to_file2 = os.path.join(os.path.dirname(__file__), '../Data/hour.csv')
hour = pd.read_csv(path_to_file2)
day = pd.read_csv(path_to_file1)

# Data Wrangling
hour['dteday'] = pd.to_datetime(hour['dteday'])
day['dteday'] = pd.to_datetime(day['dteday'])

day['mnth'] = day['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day['season'] = day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day['weekday'] = day['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day['weathersit'] = day['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Mengubah data menjadi kategorikal
day['season'] = day.season.astype('category')
hour['total_users'] = hour['casual'] + hour['registered']

# Sidebar untuk filter
st.sidebar.header('Filter Data')
year_filter = st.sidebar.selectbox('Pilih Tahun', ('2011', '2012'))
season_filter = st.sidebar.multiselect('Pilih Season', options=day['season'].unique(), default=day['season'].unique())

# Data Filtering
hour_filtered = hour[(hour['yr'] == int(year_filter)) & (hour['season'].isin(season_filter))]
day_filtered = day[day['season'].isin(season_filter)]

# Dashboard title
st.title('Bike Rental Dashboard')

# Tab structure for navigation
tab1, tab2, tab3 = st.tabs(["Overview", "Season Analysis", "Weather Impact"])

with tab1:
    st.header("Overview Data")
    st.write("Preview Hour Dataset")
    st.dataframe(hour.head())

    st.write("Preview Day Dataset")
    st.dataframe(day.head())

    st.header("Descriptive Statistics")
    st.write("Hour Dataset")
    st.dataframe(hour.describe())
    st.write("Day Dataset")
    st.dataframe(day.describe())

with tab2:
    st.header("Pengaruh Musim pada Penyewaan Sepeda")

    seasonn = day_filtered.groupby('season').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': ['max', 'min', 'mean']
    }).reindex(['Spring', 'Summer', 'Fall', 'Winter'])

    seasonn.columns = ['casual_mean', 'registered_mean', 'cnt_max', 'cnt_min', 'cnt_mean']

    fig, ax = plt.subplots(figsize=(10, 6))
    seasonn[['casual_mean', 'registered_mean']].plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e'])
    plt.title('Rata-rata Penyewaan Kasual dan Terdaftar per Musim', fontsize=16)
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Rata-rata Penyewaan', fontsize=12)
    plt.xticks(rotation=0)
    st.pyplot(fig)

with tab3:
    st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=day_filtered, x='weathersit', y='cnt', estimator=sum, ax=ax)
    plt.title('Total Penyewaan Sepeda Berdasarkan Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Total Penyewaan')
    st.pyplot(fig)
