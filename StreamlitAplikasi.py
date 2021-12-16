import pandas as pd
import matplotlib.pyplot as plt
import json
import streamlit as st

#membuka file csv dan json
df = pd.read_csv("produksi_minyak_mentah.csv")
with open("kode_negara_lengkap.json") as f :
    data_code = json.load(f)
df_json = pd.DataFrame.from_dict(data_code, orient='columns')

#mengubah tampilan streamlit menjadi lebih wide
st.set_page_config(page_title='Aplikasi Penampil Produksi Minyak', layout='wide')

#menerima inputan nama negara
name = st.text_input("Please enter the name of country : ")

#menghilangkan kode negara yang tidak ada dari json di csv
list1 = []
for i in list(df['kode_negara']) :
    if i not in list(df_json['alpha-3']) :
        list1.append(i)
    
for i in list1 :
    df = df[df.kode_negara != i]

#mengubah dari inputan nama ke kode negara
a = str()
for a in range (len(df_json)) :
    if list(df_json['name'])[a] == name :
         country_code = list(df_json['alpha-3'])[a]

#--------------PROGRAM A-----------------#

#memasukkan list tahun dan produksi negara yang dipilih
list_year = []
list_production = []
b = str()
for b in range (len(df)) : 
    if df["kode_negara"].iloc[b] == country_code :
        list_year.append(df["tahun"].iloc[b])
        list_production.append(df["produksi"].iloc[b])

#membuat plot dari jumlah produksi terhadap tahun
fig, ax = plt.subplots()
ax.set_title("Grafik Jumlah Produksi Minyak Negara Setiap Tahun",fontsize=15)
ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Produksi")
ax.plot(list_year, list_production)
plt.locator_params(axis='x', nbins=45)
plt.xticks(rotation=90,fontsize = 6)
plt.tight_layout()

graph_A = plt.show()
st.pyplot(graph_A)

#--------------PROGRAM B------------------#

#menerima inputan tahun dan jumlah negara yang diinginkan
year = []
for i in list(df['tahun']) :
    if i not in year :
        year.append(i)
T = st.selectbox("Enter the year : ", year)
T = int(T)
B = st.number_input("Enter the number of countries : ", min_value=1, key='B')
B = int(B)

#mencari data negara berdasarkan tahunnya dan diurutkan dari yang terbesar
desired_year = df.loc[df['tahun'] == T]
desired_year = desired_year.sort_values(by=['produksi'], ascending=False)
plot_desired_year = desired_year[:B]
#print(desired_year)

#membuat plot untuk negara nya
plot_desired_year.plot(kind = 'bar', x= 'kode_negara', y= 'produksi', title = 'Grafik Jumlah Produksi Minyak tiap Negara' , color = 'maroon')
graph_B = plt.show()
st.pyplot(graph_B)

#--------------PROGRAM C-----------------#

#membuat list kosong untuk menampung nilai
list2 = []
list_cumulative = []

#menerima inputan jumlah negara yang diinginkan
B2 = st.number_input("Enter the number of countries : ", min_value=1)
B2 = int(B2)

#menambahkan kode negara dalam satu list
for i in df['kode_negara'] :
    if i not in list2 :
        list2.append(i)

#menambahkan nilai produksi dalam satu list
for i in list2 :
    x = df.loc[df['kode_negara'] == i, 'produksi'].sum()
    list_cumulative.append(x)

#membuat list menjadi sebuah data frame
df_cumulative = pd.DataFrame(list(zip(list2, list_cumulative)), columns=['kode_negara', 'kumulatif'])
df_cumulative = df_cumulative.sort_values(by=['kumulatif'], ascending=False)
plot_df_cumulative = df_cumulative[:B2]

#membuat plot total kumulatif
plot_df_cumulative.plot(kind= 'bar', x='kode_negara', y='kumulatif', title = 'Grafik Jumlah Produksi Minyak Kumulatif tiap Negara' , color = 'maroon')
graph_C = plt.show()
st.pyplot(graph_C)

#-------------PROGRAM D-------------------#

#Bagian 1

#mengambil satu data dari data frame tahun tertentu
total_production = desired_year[:1].iloc[0]['produksi']
country_code2 = desired_year[:1].iloc[0]['kode_negara']
name_country = ""
region_country = ""
subregion_country = ""

#mengekstrak data spesifik dari file jason
for i in range(len(df_json)) :
    if list(df_json['alpha-3'])[i] == country_code2 :
        name_country = list(df_json['name'])[i]
        region_country = list(df_json['region'])[i]
        subregion_country = list(df_json['sub-region'])[i]

#membuat kolom
col1, col2 = st.columns(2)
with col1 :
    st.markdown("## Negara dengan jumlah produksi minyak terbesar pada tahun ",T)
    st.text(total_production)
    st.text(country_code2)
    st.text(name_country)
    st.text(region_country)
    st.text(subregion_country)

#mengambil satu data dari data frame kumulatif
total_production = df_cumulative[:1].iloc[0]['kumulatif']
country_code2 = df_cumulative[:1].iloc[0]['kode_negara']
name_country = ""
region_country = ""
subregion_country = ""

#mengekstrak data spesifik dari file jason
for i in range(len(df_json)) :
    if list(df_json['alpha-3'])[i] == country_code2 :
        name_country = list(df_json['name'])[i]
        region_country = list(df_json['region'])[i]
        subregion_country = list(df_json['sub-region'])[i]

#membuat kolom
with col2 : 
    st.markdown("## Negara dengan jumlah produksi minyak terbesar pada semua tahun ")
    st.text(total_production)
    st.text(country_code2)
    st.text(name_country)
    st.text(region_country)
    st.text(subregion_country)

#Bagian 2

#membuat data frame baru untuk nilai terkecil
df_lowvalue = desired_year[desired_year.produksi != 0]
df_lowvalue = df_lowvalue.sort_values(by=['produksi'], ascending=True)

#mengambil satu data dari data frame tahun tertentu
total_production = df_lowvalue[:1].iloc[0]['produksi']
country_code2 = df_lowvalue[:1].iloc[0]['kode_negara']
name_country = ""
region_country = ""
subregion_country = ""

#mengekstrak data spesifik dari file jason
for i in range(len(df_json)) :
    if list(df_json['alpha-3'])[i] == country_code2 :
        name_country = list(df_json['name'])[i]
        region_country = list(df_json['region'])[i]
        subregion_country = list(df_json['sub-region'])[i]

#membuat kolom
col3, col4 = st.columns(2)
with col3 :
    st.markdown("## Negara dengan jumlah produksi minyak terkecil pada tahun ",T)
    st.text(total_production)
    st.text(country_code2)
    st.text(name_country)
    st.text(region_country)
    st.text(subregion_country)

#membuat data frame baru untuk nilai terkecil (kumulatif)
df_lowvalue1 = df_cumulative[df_cumulative.kumulatif != 0]
df_lowvalue1 = df_lowvalue1.sort_values(by=['kumulatif'], ascending=True)

#mengambil satu data dari data frame tahun tertentu
total_production = df_lowvalue1[:1].iloc[0]['kumulatif']
country_code2 = df_lowvalue1[:1].iloc[0]['kode_negara']
name_country = ""
region_country = ""
subregion_country = ""

#mengekstrak data spesifik dari file jason
for i in range(len(df_json)) :
    if list(df_json['alpha-3'])[i] == country_code2 :
        name_country = list(df_json['name'])[i]
        region_country = list(df_json['region'])[i]
        subregion_country = list(df_json['sub-region'])[i]

#membuat kolom
with col4 : 
    st.markdown("## Negara dengan jumlah produksi minyak terkecil pada semua tahun")
    st.text(total_production)
    st.text(country_code2)
    st.text(name_country)
    st.text(region_country)
    st.text(subregion_country)

#Bagian 3

#membuat data frame dan list baru untuk nilai yang 0 
df_zerovalue = desired_year[desired_year.produksi == 0]
zero_country = []
zero_region = []
zero_subregion = []

#mengambil nilai dari data frame
for x in range(len(df_zerovalue)) :
    for y in range(len(df_json)) :
        if list(desired_year["kode_negara"])[x] == list(df_json['alpha-3'])[y] :
            zero_country.append(list(df_json['name'])[y])
            zero_region.append(list(df_json['region'])[y])
            zero_subregion.append(list(df_json['sub-region'])[y])

#memasukkan nilai sebelumnya ke dalam data frame nilai 0
df_zerovalue['negara'] = zero_country
df_zerovalue['region'] = zero_region
df_zerovalue['sub-region'] = zero_subregion

#membuat data frame dan list baru untuk nilai yang 0 (kumulatif)
df_zerovalue1 = df_cumulative[df_cumulative.kumulatif == 0]
zero_country_cumulative = []
zero_region_cumulative = []
zero_subregion_cumulative = []

#mengambil nilai dari data frame
for x in range(len(df_zerovalue1)) :
    for y in range(len(df_json)) :
        if list(df_cumulative["kode_negara"])[x] == list(df_json['alpha-3'])[y] :
            zero_country_cumulative.append(list(df_json['name'])[y])
            zero_region_cumulative.append(list(df_json['region'])[y])
            zero_subregion_cumulative.append(list(df_json['sub-region'])[y])

#memasukkan nilai sebelumnya ke dalam data frame nilai 0
df_zerovalue1['negara'] = zero_country_cumulative
df_zerovalue1['region'] = zero_region_cumulative
df_zerovalue1['sub-region'] = zero_subregion_cumulative

st.table(df_zerovalue)
st.table(df_zerovalue1)