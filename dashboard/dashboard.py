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

bins_hum = [0, 0.33, 0.66, 1] # Membuat rentang kategori untuk kelembapan
labels = ['Low Humidity', 'Medium Humidity', 'High Humidity']
hour['humidity_category'] = pd.cut(hour['hum'], bins=bins_hum, labels=labels)

# Mengelompokkan data berdasarkan kategori kelembapan
humidity_rentals = hour.groupby('humidity_category').agg({
    'cnt': ['mean', 'sum']
}).reset_index()
humidity_rentals.columns = ['Humidity Level', 'Average Rentals', 'Total Rentals']

bins_win =[0, 0.283, 0.567, 0.8507] # Membuat rentanf kategori untuk kecepatan angin
labels = ['Low Windspeed', 'Medium Windspeed', 'High Windspeed']
hour['windspeed_category'] = pd.cut(hour['windspeed'], bins=bins_win, labels=labels)
windspeed_rentals = hour.groupby('windspeed_category').agg({
    'cnt': ['mean', 'sum']
}).reset_index()
windspeed_rentals.columns = ['Windspeed Level', 'Average Rentals', 'Total Rentals']


# Membuat sidebar filter
st.sidebar.header('Filter Data')
year_filter = st.sidebar.selectbox('Pilih Tahun', ('2011', '2012'))
season_filter = st.sidebar.multiselect('Pilih Season', options=day['season'].unique(), default=day['season'].unique())

# Data Filtering
hour_filtered = hour[(hour['yr'] == int(year_filter)) & (hour['season'].isin(season_filter))]
day_filtered = day[day['season'].isin(season_filter)]

# Dashboard title
st.title('Bike Rental Dashboard')

# Tab structure for navigation
tab1, tab2 = st.tabs(["Season Analysis", "Weather Impact"])

with tab1:
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

with tab2:
    st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda")

    # Membuat figure dan dua sumbu
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(humidity_rentals['Humidity Level'], humidity_rentals['Total Rentals'], color='skyblue', alpha=0.7, label='Total Rentals')
    ax1.set_title('Penyewaan Sepeda Berdasarkan Kategori Kelembapan')
    ax1.set_xlabel('Kategori Kelembapan')
    ax1.set_ylabel('Jumlah Penyewaan')
    ax1.legend()
    ax1.grid(axis='y')

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(humidity_rentals['Humidity Level'], humidity_rentals['Average Rentals'], color='skyblue', alpha=0.7, label='Average Rentals')
    ax2.set_title('Rata-Rata Penyewaan Sepeda Berdasarkan Kategori Kelembapan')
    ax2.set_xlabel('Kategori Kelembapan')
    ax2.set_ylabel('Jumlah Penyewaan')
    ax2.legend()
    ax2.grid(axis='y')


    col1, col2 = st.columns(2)
    st.subheader("Pengaruh Kelembapan Terhadap Penyewaan Sepeda" )
    col3, col4 = st.columns(2)
    st.subheader("Pengaruh Kecepatan Angin Terhadap Penyewaan Sepeda" )
    col5, col6 = st.columns(2)

    with col1:
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=day, x='weathersit', y='cnt', estimator='sum', color='skyblue')
        plt.title('Total Penyewaan Sepeda Berdasarkan Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Total Penyewaan')
        plt.grid(axis='y')
        st.pyplot(plt.gcf())  # Menampilkan grafik di Streamlit
    
    with col2:
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=day, x='weathersit', y='cnt', estimator='mean', color='skyblue')
        plt.title('Total Penyewaan Sepeda Berdasarkan Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Total Penyewaan')
        plt.grid(axis='y')
        st.pyplot(plt.gcf())  # Menampilkan grafik di Streamlit

    with col3:
        st.pyplot(fig1)

    with col4:
        st.pyplot(fig2)

    with col5:
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='Windspeed Level', y='Total Rentals', data=windspeed_rentals, color='orange', marker='o', label='Total Rentals', ax=ax1)
        ax1.set_title('Penyewaan Sepeda Berdasarkan Kategori Kecepatan Angin')
        ax1.set_xlabel('Kategori Kecepatan Angin')
        ax1.set_ylabel('Jumlah Penyewaan')
        ax1.legend()
        ax1.grid(axis='y')
        st.pyplot(fig1)

    # Plot kedua: Rata-Rata Penyewaan Berdasarkan Kategori Kecepatan Angin
    with col6:
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='Windspeed Level', y='Average Rentals', data=windspeed_rentals, color='orange', marker='o', label='Average Rentals', ax=ax2)
        ax2.set_title('Rata-Rata Penyewaan Sepeda Berdasarkan Kategori Kecepatan Angin')
        ax2.set_xlabel('Kategori Kecepatan Angin')
        ax2.set_ylabel('Jumlah Penyewaan')
        ax2.legend()
        ax2.grid(axis='y')
        st.pyplot(fig2)
