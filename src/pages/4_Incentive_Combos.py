import streamlit as st
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.express as px

df = pd.read_excel('C:\AIML\HackNiche_DODS\Streamlit_Interface\src\pages\streamlit_data\HackNicheDataset.xlsx', 'Sales Dump')

def set_to_str(itemset):
    return ', '.join(list(itemset))

def return_itemset(df2):
    # Ensure to use the passed dataframe (df2) for analysis
    te = TransactionEncoder()
    item_lists = df2.groupby('Invoice No.')['Item Name'].agg(lambda x: list(x)).tolist()
    te_ary = te.fit_transform(item_lists)
    df_onehot = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_itemsets = apriori(df_onehot, min_support=0.007, use_colnames=True, max_len=5)
    frequent_itemsets['NumItem'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    frequent_itemsets['itemsets_str'] = frequent_itemsets['itemsets'].apply(set_to_str)

    return frequent_itemsets

st.title('Frequent Itemsets Analysis')
st.write("#### Generate insights from your sales data effortlessly with this feature. Customize parameters such as date range and order type, then click Compute to unveil top frequent itemsets with at least two items. Visualize these patterns in an interactive bar chart to discern common purchase trends.")
st.sidebar.subheader('Customize Parameters')
from_date = st.sidebar.date_input('From Date', pd.to_datetime('2024-01-20'))
to_date = st.sidebar.date_input('To Date', pd.to_datetime('2024-01-22'))
from_date = pd.to_datetime(from_date)
to_date = pd.to_datetime(to_date)
order_type = st.sidebar.selectbox('Order Type', df['Order Type'].unique())
compute = st.sidebar.button('Compute')

if compute:
    # Filter based on sidebar inputs
    filtered_df = df[(df['Timestamp'] >= from_date) & (df['Timestamp'] <= to_date) & (df['Order Type'] == order_type)]
    
    # Pass the filtered_df to the return_itemset function
    frequent_itemsets_filtered = return_itemset(filtered_df)
    freqItemsetMore2_filtered = frequent_itemsets_filtered[frequent_itemsets_filtered['NumItem'] >= 2]
    
    st.write("Here are the frequent itemsets with at least two items:")
    fig = px.bar(freqItemsetMore2_filtered.head(20), x='support', y='itemsets_str', orientation='h', height=600, width=800, title='Top 20 Frequent Itemsets after Filtering')
    st.plotly_chart(fig)
else:
    # Initial plot or default view before filtering
    frequent_itemsets = return_itemset(df)
    freqItemsetMore2 = frequent_itemsets[frequent_itemsets['NumItem'] >= 2]
    fig = px.bar(freqItemsetMore2.head(20), x='support', y='itemsets_str', orientation='h', height=600, width=800, title='Top 20 Frequent Itemsets')
    st.plotly_chart(fig)
