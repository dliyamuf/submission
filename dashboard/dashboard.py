import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#menyiapkan dataframe
#membuat dataframe daily_orders
# def func_daily_orders(data):
#     daily_orders = data.groupby(['date', 'order_id_x']).agg({
#         'price': 'sum'
#     })
#     daily_orders = daily_orders.reset_index()
#     daily_orders.rename(columns={
#         'order_id_x': 'order_count',
#         'price': 'revenue'
#     }, inplace=True
#     )
#     return daily_orders

#membuat dataframe monthly orders
# def func_monthly_orders(data):
#     monthly_orders = data.groupby('year_month').agg({
#         'order_id_x' : 'nunique',
#         'price': 'sum'
#     })
#     monthly_orders = monthly_orders.reset_index()
#     monthly_orders.rename(columns={
#         'order_id_x': 'order_count',
#         'price': 'revenue'
#     }, inplace=True
#     )
#     return monthly_orders

#membuat dataframe top 5 product category
def func_top_5_product(data):
    monthly_order = data.groupby(['year_month', 'product_category_name_english']).agg({'price': 'sum'}).reset_index()
    total_order_per_category = monthly_order.groupby('product_category_name_english')['price'].mean()
    top_5_price_product = total_order_per_category.nlargest(5).index
    top_5_product = monthly_order[monthly_order['product_category_name_english'].isin(top_5_price_product)]
    return top_5_product

#membuat dataframe persebaran pembeli berdasarkan state
def func_by_state(df):
    by_state = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    by_state.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return by_state

#membuat dataframe rfm analysis
def func_rfm(df):
    rfm = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max", #mengambil tanggal order terakhir
        "order_id_x": "nunique",
        "price": "sum"
    })
    rfm.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm["max_order_timestamp"] = rfm["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm["recency"] = rfm["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm

#memanggil main_data.csv
url='https://drive.google.com/file/d/1DJniWK38Abf0ZVhA9T014nqjH3ZT1EY8/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
main_data = pd.read_csv(url)

#mengubah dan mengurutkan main_data berdasarkan datetime
# datetime_columns = ["order_purchase_timestamp"]
# main_data.sort_values(by="year_month", inplace=True)
# main_data.reset_index(inplace=True)
 
# for column in datetime_columns:
#     main_data[column] = pd.to_datetime(main_data[column])

 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://files.klob.id/public/mig01/l32ovhf5/channels4_profile.jpg")
    

#memanggil fungsi yang sudah dibuat
# daily_orders = func_daily_orders(main_data)
# monthly_orders = func_monthly_orders(main_data)
top_5_product = func_top_5_product(main_data)
by_state = func_by_state(main_data)
rfm = func_rfm(main_data)

#MEMBUAT HEADER
st.header("BRAZILIAN E-COMMERCE DASHBOARD")

#MENAMBAHKAN SUBHEADER
#membuat visualisasi daily orders
# st.subheader('Daily Orders')
 
# col1, col2 = st.columns(2)
 
# with col1:
#     total_orders = daily_orders.order_count.sum()
#     st.metric("Total orders", value=total_orders)
 
# with col2:
#     total_revenue = daily_orders.revenue.sum()
#     st.metric("Total Revenue", value=total_revenue)
 
# fig, ax = plt.subplots(figsize=(16, 8))
# ax.plot(
#     daily_orders["order_purchase_timestamp"],
#     daily_orders["order_count"],
#     marker='o', 
#     linewidth=2,
#     color="#f3584b"
# )
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)
 
# st.pyplot(fig)
#menambahkan visualisasi monthly orders
# st.subheader('Monthly Orders')
 
# col1, col2 = st.columns(2)
 
# with col1:
#     total_orders = monthly_orders.order_count.sum()
#     st.metric("Total orders", value=total_orders)
 
# with col2:
#     total_revenue = monthly_orders.revenue.sum()
#     st.metric("Total Revenue", value=total_revenue)
 
# fig, ax = plt.subplots(figsize=(16, 8))
# ax.plot(
#     monthly_orders["year_month"],
#     monthly_orders["order_count"],
#     marker='o', 
#     linewidth=2,
#     color="#f3584b"
# )
# ax.tick_params(axis='y', labelsize=20)
# ax.tick_params(axis='x', labelsize=15)
 
# st.pyplot(fig)

#menambahkan visualisasi top 5 product category
colors = ["#78281f", "#d74d42", "#f3584b", "#f1948a", "#fadbd8"]
plt.figure(figsize=(15, 8))
sns.lineplot(data=top_5_product, x='year_month', y='price', hue='product_category_name_english', marker='o', linestyle='-')
plt.title('Monthly Sales of Top 5 Product Category')
plt.xticks(rotation=90)

#menambahkan visualisasi customer demographics
st.subheader("Customer Demographics")
 
fig, ax = plt.subplots(figsize=(20, 10))
 
sns.barplot(
        y="customer_count", 
        x="customer_state",
        data=by_state.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Number of Customer by State", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
 

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
