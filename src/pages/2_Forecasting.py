from prophet import Prophet
import pandas as pd
import numpy as np
import streamlit as st

df= pd.read_excel(r"v3dit/aggregators/src/pages/tsa_data.xlsx")
model = Prophet()

df['Date'] = pd.to_datetime(df['Timestamp']).dt.date

# Aggregate sales data
aggregated_sales = df.groupby(['Date', 'Item Name']).agg({'Qty.': 'sum'}).reset_index()

# Rename columns for Prophet compatibility
aggregated_sales.rename(columns={'Date': 'ds', 'Qty.': 'y'}, inplace=True)


st.title('Item Sales Forecasting')
st.write('This feature helps you forecast future sales of menu items with ease. Just choose an item and set the forecast period to generate valuable insights. Use this data to smartly manage inventory and improve customer satisfaction.')
st.write("### *A simple web application to predict future sales of different items in a store*")

# Item selection
item_name = st.selectbox('Select Item Name', options=aggregated_sales['Item Name'].unique())
time_period = st.number_input('Enter the number of days for prediction', min_value=1, max_value=365, value=5)
# Forecasting function
def forecast_sales(item_name,time_period):
    # Filter data for the selected item
    item_data = aggregated_sales[aggregated_sales['Item Name'] == item_name]
    
    # Initialize and fit the Prophet model
    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.fit(item_data[['ds', 'y']])
    
    # Create future dataframe
    future = model.make_future_dataframe(periods=time_period)  # Forecasting for the next 90 days
    
    # Forecast
    forecast = model.predict(future)
    
    # Plotting
    fig = model.plot(forecast)
    return fig, forecast

# Forecast button
if st.button('Forecast Sales'):
    fig, forecast = forecast_sales(item_name,time_period)
    
    # Display the forecast graph
    st.write(f'Forecast for {item_name}')
    st.pyplot(fig)
    
    # Optional: Display forecast components
    fig_comp = model.plot_components(forecast)
    st.pyplot(fig_comp)
    
    # Conclusions based on the forecast
    # Here you can add any conclusions or insights you derive from the forecast
    st.write("Conclusions and insights based on the forecast can be discussed here.")

