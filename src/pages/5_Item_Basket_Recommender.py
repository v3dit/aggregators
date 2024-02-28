import streamlit as st
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.express as px

# Read datanew_df.transpose().rename(columns=new_df['ItemName'])
recipedf = pd.read_csv('v3dit/aggregators/src/pages/streamlit_data/Recipes_encoded.csv')
recipedf = recipedf.transpose().rename(columns=recipedf['ItemName'])
df = pd.read_excel('v3dit/aggregators/src/pages/streamlit_data/HackNicheDataset.xlsx', 'Sales Dump')
st.title('Item Basket Recommender')
st.write('#### This feature analyzes sales data and provides personalized item recommendations based on user-selected items and allergies. After choosing bought items and allergies, click "Generate Recommendations" to receive tailored suggestions. View bought items and recommendations displayed with buttons for easy navigation.')

# Drop unnecessary columns
df2 = df.drop(columns=['Date', 'Timestamp', 'Payment Type', 'Order Type', 'Area',  
                       'Price', 'Qty.', 'Sub Total', 'Discount', 'Tax', 'Final Total',
                       'Status', 'Table No.', 'Server Name', 'Covers', 'Variation',
                       'Category', 'HSN', 'Phone', 'Name', 'Address', 'GST', 'Assign To',
                       'Non Taxable', 'CGST Rate', 'CGST Amount', 'SGST Rate',
                       'SGST Amount', 'VAT Rate', 'VAT Amount', 'Service Charge Rate',
                       'Service Charge Amount'])

# Transaction Encoding
te = TransactionEncoder()
item_lists = df2.groupby('Invoice No.')['Item Name'].agg(lambda x: list(x)).tolist()
te_ary = te.fit_transform(item_lists)
df_onehot = pd.DataFrame(te_ary, columns=te.columns_)

# Find frequent itemsets
frequent_itemsets = apriori(df_onehot, min_support=0.007, use_colnames=True, max_len=5)
frequent_itemsets['NumItem'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
freqItemsetMore2 = frequent_itemsets[frequent_itemsets['NumItem'] >= 2]
def set_to_str(itemset):
    return ', '.join(list(itemset))
freqItemsetMore2['itemsets_str'] = freqItemsetMore2['itemsets'].apply(set_to_str)
# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)



bought_items = st.multiselect('Select items you bought:', df['Item Name'].unique() )

# if bought_items:
#     st.write("You bought:") 
#     for item in bought_items:
#         st.write(f"- {item}") 
# else:
#     st.write("Buy some items to get recommendations.")
    
    # Function to recommend items based on current basket
def isallergic(item,allergies):
    flag=0
    for allergy in allergies:
        flag+=recipedf[item][allergy]
    return flag
# st.write(recipedf['South Indian Filter Kaapi (250 ML)'])
def recommend_items(current_items, rules, allergies):
    recommendations = set()
    for item in current_items:
        relevant_rules = rules[rules['antecedents'] == {item}]
        for index, rule in relevant_rules.iterrows():
            consequents = set(rule['consequents'])
            recommendations.update(consequents)
            
    recommendations_stripped = [item for item in recommendations if item!='South Indian Filter Kaapi (150 ML)' and isallergic(item, allergies) == 0]
    return set(recommendations_stripped)


# Get allergies from user input (e.g., via another dropdown)
allergies = st.multiselect('Select your allergies:', recipedf.index)

# Get recommendations based on bought items and allergies
recommendations = recommend_items(bought_items, rules, list(allergies))
recommendations = recommendations - set(bought_items)
# Display recommendations
st.write("Recommended items:")
# if recommendations:
#     for item in recommendations:
#         st.write(f"- {item}")
# else:
#     st.write("No recommendations found.")
# print(list(recommendations))
# Display bought items and recommendations using buttons with colors and inline CSS
def add_to_bought(item):
    bought_items.append(item)
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Bought Items")
    for item in bought_items:
        st.markdown(
            f'<button style="background-color: #7CB9E8; border-radius:8px;border: none; color: white; padding: 8px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">{item}</button>',
            unsafe_allow_html=True
        )

with col2:
    st.subheader("Recommended Items")
    if recommendations:
        for item in recommendations:
            st.markdown(
                f'<button style="background-color: #32de84; border-radius:8px;border: none; color: white; padding: 8px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">{item}</button>',
                unsafe_allow_html=True
            )
    else:
        st.write("No recommendations found.")