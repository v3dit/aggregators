import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_excel('v3dit/aggregators/src/pages/streamlit_data/HackNicheDataset.xlsx', 'Sales Dump')
# df = pd.read_excel('EttarraDataset.xlsx', 'Sales Data')

# Function to calculate sales data
def calculate_sales(df):
    sales_data = df.groupby('Item Name')['Qty.'].sum().reset_index()
    sales_data = sales_data.sort_values(by='Qty.', ascending=False)
    return sales_data

# Streamlit UI setup
st.title('Least and Most Sold Items')
st.write("#### This feature provides insights into your sales data, allowing you to customize parameters like date range and order type. Upon clicking Compute, discover the most and least sold items, along with summary statistics such as total spending, average price per item, and the most common order type. Visualize the top 20 most sold items in an interactive bar chart.")
# Sidebar for user input
st.sidebar.title('Customize Parameters')
from_date = st.sidebar.date_input('From Date', pd.to_datetime('2024-01-01'))
to_date = st.sidebar.date_input('To Date', pd.to_datetime('2024-01-31'))
from_date = pd.to_datetime(from_date)
to_date = pd.to_datetime(to_date)
order_type = st.sidebar.selectbox('Order Type', df['Order Type'].unique())
compute = st.sidebar.button('Compute')

if compute:
    # Filter the dataframe based on user input
    filtered_df = df[(df['Timestamp'] >= from_date) & (df['Timestamp'] <= to_date) & (df['Order Type'] == order_type)]

    # Calculate sales data for the filtered dataframe
    sales_data = calculate_sales(filtered_df)


    # Display most and least sold items
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Most Sold Items:')
        for item in sales_data['Item Name'].head():
            st.success(item)

    with col3:
        st.subheader('Least Sold Items:')
        for item in sales_data['Item Name'].tail().iloc[::-1]:
            st.error(item)
    
    # Display summary statistics
    total_sales = filtered_df['Qty.'].sum()
    total_price = filtered_df['Final Total'].sum()
    avg_price_per_item = total_price / total_sales if total_sales else 0
    st.write(f"With your current selection, you've spent ₹{total_price:.2f} on {total_sales} items.")
    st.write(f"The average price per item is ₹{avg_price_per_item:.2f}.")

    # Display spending information with markdown
    st.markdown(
        f"<div style='padding: 20px; border-radius: 8px; display: grid; grid-template-columns: 1fr 1fr; grid-gap: 20px;'>"
        f"<div style='font-size: 18px; padding: 20px; border-radius: 8px; display: grid; background-color: #B9F3FC; text-align:center; font-size:22px;'><b>Total Spending:</b><br>₹{total_price:.2f}</div>"
        f"<div style='font-size: 18px; padding: 20px; border-radius: 8px; display: grid; background-color: #93C6E7; text-align:center; font-size:22px;'><b>Total Items:</b><br>{total_sales}</div>"
        f"<div style='font-size: 18px; padding: 20px; border-radius: 8px; display: grid; background-color: #AEE2FF; text-align:center; font-size:22px;'><b>Average Price per Item:</b><br>₹{avg_price_per_item:.2f}</div>"
        f"<div style='font-size: 18px; padding: 20px; border-radius: 8px; display: grid; background-color: #FEDEFF; text-align:center; font-size:22px;'><b>Most Common Order Type:</b><br>{filtered_df['Order Type'].value_counts().idxmax()}</div>"
        "</div>", unsafe_allow_html=True
    )

    # Plot the top 20 most sold items
    fig = px.bar(sales_data.head(20), x='Qty.', y='Item Name', orientation='h', height=600, width=800, title='Top 20 Most Sold Items')
    st.plotly_chart(fig)
else:
    st.header("Press 'Compute' to get the most and least sold items.")