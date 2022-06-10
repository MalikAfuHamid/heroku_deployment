import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import ttest_1samp
from scipy import stats
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Milestone Visualization",
    layout="centered",
    initial_sidebar_state="expanded"
)

df = pd.read_csv('bq-results-20220609-034636-1654746413021.csv', parse_dates = ['created_at','delivered_at','shipped_at'])

created_dt = df.created_at.dt
df['year_created_at'] = created_dt.year
df['month_created_at'] = created_dt.month
df['day_created_at'] = created_dt.dayofweek
df['hour_created_at'] = created_dt.hour
df.drop(columns = 'created_at', inplace = True)


delivered_dt = df.delivered_at.dt
df['year_delivered_at'] = delivered_dt.year
df['month_delivered_at'] = delivered_dt.month
df['day_delivered_at'] = delivered_dt.dayofweek
df['hour_delivered_at'] = delivered_dt.hour
df.drop(columns = 'delivered_at', inplace = True)

shipped_dt = df.shipped_at.dt
df['shipped_at'] = shipped_dt.year
df['shipped_at'] = shipped_dt.month
df['shipped_at'] = shipped_dt.dayofweek
df['shipped_at'] = shipped_dt.hour
df.drop(columns = 'shipped_at', inplace = True)

df2 = df.copy()
df2.year_delivered_at = df2['year_delivered_at'].fillna('Tidak diketahui')
df2.month_delivered_at = df2['month_delivered_at'].fillna('Tidak diketahui')
df2.day_delivered_at = df2['day_delivered_at'].fillna('Tidak diketahui')
df2.hour_delivered_at = df2['hour_delivered_at'].fillna('Tidak diketahui')
df2 = df2[~df.city.isna()]
df2 = df2[~df.product_name.isna()]
a = df2[df2['status'] == 'Complete']['sale_price']
b = df2[df2['status'] == 'Complete']['cost']

df2['profit'] = a - b
df2.profit.fillna(0, inplace = True)




option = st.sidebar.selectbox('',
    ['Visualization', 'Analysis'])

if option == 'Visualization':
    st.subheader('Negara apa yang memberikan rata-rata profit setiap bulannya?')
    country_profit= df2.groupby(['country'])['profit'].mean().sort_values(ascending = False)
    country_profit = country_profit.reset_index()
    st.write(country_profit)
    
    fig1 = plt.figure(figsize=(18,6))
    ax1 = sns.barplot(x='country', y='profit', data=country_profit)

    plt.title('Profit Ecommerce Berdasarkan Asal Negara Setiap Bulan')
    st.pyplot(fig1)
    

    st.subheader('Berapa umur rata-rata orang yang membeli produk dengan kategori tertentu?')
    age_var = df2.groupby('product_category')['age'].mean()
    age_var = age_var.reset_index()
    st.write(age_var)

    fig2 = plt.figure(figsize=(10,8))
    ax2 = sns.barplot(x='product_category', y='age', data=age_var)

    plt.setp(ax2.get_xticklabels(), rotation=90)
    plt.title('Umur rata-rata orang yang membeli produk dengan kategori tertentu')
    st.pyplot(fig2)

    st.subheader('Apa 10 produk yang memberikan rata-rata keuntungan paling tinggi?')
    product_profit = df2.groupby('product_name')['profit'].mean().sort_values(ascending= False).head(10)
    product_profit = product_profit.reset_index()
    st.write(product_profit)



    fig3 = plt.figure(figsize=(10,15))
    ax3 = sns.barplot(x='product_name', y='profit', data=product_profit)

    plt.setp(ax3.get_xticklabels(), rotation=90)
    plt.title('10 Produk yang Memberikan Rata-rata Keuntungan paling tinggi')
    st.pyplot(fig3)


    st.subheader('10 Kategori produk apa yang memberikan rata-rata profit paling tinggi pada ecommerce?')
    categoric_profit = df2.groupby('product_category')['profit'].mean().sort_values(ascending=False).head(10)
    categoric_profit = categoric_profit.reset_index()
    
    
    fig4 = plt.figure(figsize=(10,8))
    ax4 = sns.barplot(x='product_category', y='profit', data=categoric_profit)
    st.write(categoric_profit)

    plt.setp(ax4.get_xticklabels(), rotation=65)
    plt.title('10 Kategori Produk yang Memberikan Rata-rata Keuntungan paling Tinggi')
    st.pyplot(fig4)

    st.subheader('Siapa pelanggan yang paling banyak dalam memberikan keuntungan terhadap ecommerce?')
    name_profit = df2.groupby('name')['profit'].mean().sort_values(ascending=False).head(10)
    name_profit = name_profit.reset_index()
    st.write(name_profit)

    fig5 = plt.figure(figsize=(10,8))
    ax5 = sns.barplot(x='name', y='profit', data=name_profit)

    plt.setp(ax5.get_xticklabels(), rotation=65)
    plt.title('10 Nama orang yang paling banyak memberikan keuntungan')
    st.pyplot(fig5)
    

else:
    st.subheader('Analisis Inferensial Statistik')
    country_profit= df2.groupby(['country'])['profit'].mean().sort_values(ascending = False)
    country_profit = country_profit.reset_index()


    df_Austria = df2[df2.country == 'Austria']
    df_Colombia = df2[df2.country == 'Colombia']
    stat, p_value = ttest_1samp(df_Colombia['profit'], 15.542247)
    nilai = np.random.normal(df_Colombia['profit'].mean(), df_Colombia['profit'].std(), 10000)

    ci = stats.norm.interval(0.95, df_Colombia['profit'].mean(), df_Colombia['profit'].std())

    fig6 = plt.figure(figsize=(16,5))
    sns.distplot(nilai, label='Amount with Outlier Removed (Population)', color='blue')
    plt.axvline(df_Colombia['profit'].mean(), color='red', linewidth=2, label='Amount with Outlier Removed (Mean)')

    plt.axvline(ci[1], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
    plt.axvline(ci[0], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')

    plt.axvline(nilai.mean() + stat*nilai.std(), color='black', linestyle='dashed', linewidth=2, label = 'Alternative Hypothesis')
    plt.axvline(nilai.mean() - stat*nilai.std(), color='black', linestyle='dashed', linewidth=2)
    plt.legend()
    st.pyplot(fig6)
    st.write('Berdasarkan hasil perhitungan dan visualisasi di atas, maka p value berada di dalam area dari confidence interval sehingga pernyataan tidak ada perbedaan yang signifikan antara-rata-rata profit yang di dapatkan dari negara Austria dan Colombia diterima')
    st.write('Dari hasil analsisi yang dilakukan terhadapn the look ecommerce, maka masih banyak yang bisa diperhatikan dari CEO untuk meningkatkan profit ecommerce. Terlebih, terdapat ketidaksesuaian antara status pengiriman dengan profit.')
   




























































































