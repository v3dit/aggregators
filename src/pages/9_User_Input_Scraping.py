import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Load the data
def load_data():
    # Replace this path with the actual path to your cleaned competitors CSV file
    file_path = 'v3dit/aggregators/src/pages/cleaned_competitors_final.csv'
    return pd.read_csv(file_path)

data = load_data()

# Extracting Ettara Coffee's data
ettara_coffee_data = data[data['Name'].str.contains('Ettara|Ettarra', case=False, regex=True)].iloc[0]

# Function to scrape data from a given URL
def scrape_data(url):
    # Initialize the web driver (ensure the driver path is correct for your setup)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)

    # Name
    name_elements = driver.find_elements(By.TAG_NAME, 'h1')
    name = name_elements[0].text if name_elements else "N/A"

    # Ratings
    ratings = driver.find_elements(By.CSS_SELECTOR, '.sc-1q7bklc-1.cILgox')   # More Info
    ratings = ratings[0].text if ratings else "N/A"
    
    # Cuisines
    cuisines = driver.find_elements(By.CSS_SELECTOR, '.sc-fuzEkO.iXqdwC')
    cuisines = ', '.join([element.text for element in cuisines]) if cuisines else "N/A"
    
    # Average Cost
    avg_cost = driver.find_elements(By.CSS_SELECTOR, '.sc-1hez2tp-0')
    avg_cost = [element.text.split("for")[0].strip() for element in avg_cost if "₹" in element.text]
    avg_cost = avg_cost[0] if avg_cost else "N/A"
    
    # Known For
    body_text = driver.find_element(By.TAG_NAME, "body").text
    known_for_start = "People Say This Place Is Known For"
    known_for_end = "Average Cost"
    known_for = body_text[body_text.find(known_for_start)+len(known_for_start):body_text.find(known_for_end)].strip() or "N/A"
    
    # Frequent Searches
    freq_start = "FREQUENT SEARCHES LEADING TO THIS PAGE"
    freq_end = "TOP STORES"
    frequent_searches = body_text[body_text.find(freq_start)+len(freq_start):body_text.find(freq_end)].strip() or "N/A"
    
    # Close the driver
    driver.quit()

    return name, ratings, cuisines, avg_cost, known_for, frequent_searches

# Streamlit UI setup
st.title('Ettarra Coffee vs. Competitor Scraper')
st.write('Enter the URL of a competitor\'s page to scrape the necessary attributes and compare with Ettarra Coffee.')

# Input field for URL
url_input = st.text_input('Enter the URL:', '')

# Button to trigger scraping and comparison
if st.button('Scrape and Compare'):
    if url_input:
        # Scrape data from the provided URL
        competitor_name, competitor_ratings, competitor_cuisines, competitor_avg_cost, competitor_known_for, competitor_frequent_searches = scrape_data(url_input)

        # Display the comparison table
        comparison_data = {
            'Attribute': ['Name', 'Ratings', 'Cuisines', 'Average Cost', 'Known For', 'Frequent Searches'],
            'Ettarra Coffee': ['Ettarra Coffee', ettara_coffee_data['Ratings'], ettara_coffee_data['Cuisines'], f"${ettara_coffee_data['Average Cost']} for 2", ettara_coffee_data['Known For'], ettara_coffee_data['Frequent Searches']],
            competitor_name: [competitor_name, competitor_ratings, competitor_cuisines, f"${competitor_avg_cost} for 2", competitor_known_for, competitor_frequent_searches]
        }
        comparison_df = pd.DataFrame(comparison_data)

        st.write('Comparison Table:')
        st.table(comparison_df)
        st.button('Generate Insights')
    else:
        st.warning('Please enter a valid URL.')
