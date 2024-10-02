import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#memanggil main_data.csv
url='https://drive.google.com/file/d/1DJniWK38Abf0ZVhA9T014nqjH3ZT1EY8/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
main_data = pd.read_csv(url)

rfm = main_data.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max", # mengambil tanggal order terakhir
    "order_id": "nunique", # menghitung jumlah order
    "price": "sum" # menghitung jumlah revenue yang dihasilkan
})

rfm.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

#menghitung kapan terakhir pelanggan melakukan transaksi (hari)
rfm["max_order_timestamp"] = rfm["max_order_timestamp"].dt.date
recent_date = clean_data_order_product_english["order_purchase_timestamp"].dt.date.max()
rfm["recency"] = rfm["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://files.klob.id/public/mig01/l32ovhf5/channels4_profile.jpg")
    


#menambahkan visualisasi RFM
st.subheader("Best Customer Based on RFM Parameters")
 
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(15, 15))
 
colors = ["#78281f", "#d74d42", "#f3584b", "#f1948a", "#fadbd8"]
 
sns.barplot(x="recency", y="customer_id", data=rfm.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)
 
sns.barplot(x="frequency", y="customer_id", data=rfm.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
 
sns.barplot(x="monetary", y="customer_id", data=rfm.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
 
st.caption('Bangkit Academy 2024 Batch 2')
