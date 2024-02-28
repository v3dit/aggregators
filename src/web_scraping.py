from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Initialize the web driver (ensure the driver path is correct for your setup)
driver = webdriver.Chrome()
url_list = [
    "https://www.zomato.com/mumbai/blabber-all-day-juhu",
    "https://www.zomato.com/mumbai/ananda-cafe-juhu",
    "https://www.zomato.com/mumbai/third-wave-coffee-juhu",
    "https://www.zomato.com/mumbai/javaphile-pali-hill-bandra-west",
    "https://www.zomato.com/mumbai/earth-cafe-@-juhu-1-juhu",
    "https://www.zomato.com/mumbai/love-latte-juhu",
    "https://www.zomato.com/mumbai/masa-bakery-juhu",
    "https://www.zomato.com/mumbai/prithvi-cafe-juhu",
    "https://www.zomato.com/mumbai/silver-beach-cafe-juhu",
    "https://www.zomato.com/mumbai/ettarra-1-juhu"
]

# Lists to store data
numbers_list=[]
num=0
names_list=[]
ratings_list = []
cuisines_list = []
avg_cost_list = []
known_for_list = []
frequent_searches_list = []

for url in url_list:
    driver.get(url)
    time.sleep(10)
    
    numbers_list.append(num)
    num+=1
    
    # Name
    name_elements = driver.find_elements(By.TAG_NAME, 'h1')
    name = name_elements[0].text if name_elements else "N/A"
    names_list.append(name)

    # Ratings
    ratings = driver.find_elements(By.CSS_SELECTOR, '.sc-1q7bklc-1.cILgox')   # More Info
    ratings = ratings[0].text if ratings else "N/A"
    ratings_list.append(ratings)
    
    # Cuisines
    cuisines = driver.find_elements(By.CSS_SELECTOR, '.sc-fuzEkO.iXqdwC')
    cuisines = ', '.join([element.text for element in cuisines]) if cuisines else "N/A"
    cuisines_list.append(cuisines)
    
    # Average Cost
    avg_cost = driver.find_elements(By.CSS_SELECTOR, '.sc-1hez2tp-0')
    avg_cost = [element.text.split("for")[0].strip() for element in avg_cost if "₹" in element.text]
    avg_cost = avg_cost[0] if avg_cost else "N/A"
    avg_cost_list.append(avg_cost)
    
    # Known For
    body_text = driver.find_element(By.TAG_NAME, "body").text
    known_for_start = "People Say This Place Is Known For"
    known_for_end = "Average Cost"
    known_for = body_text[body_text.find(known_for_start)+len(known_for_start):body_text.find(known_for_end)].strip() or "N/A"
    known_for_list.append(known_for)
    
    # Frequent Searches
    freq_start = "FREQUENT SEARCHES LEADING TO THIS PAGE"
    freq_end = "TOP STORES"
    frequent_searches = body_text[body_text.find(freq_start)+len(freq_start):body_text.find(freq_end)].strip() or "N/A"
    frequent_searches_list.append(frequent_searches)

# Combine lists into DataFrame
df = pd.DataFrame({
    "":numbers_list,
    "Name": names_list, 
    "Ratings": ratings_list,
    "Cuisines": cuisines_list,
    "Average Cost": avg_cost_list,
    "Known For": known_for_list,
    "Frequent Searches": frequent_searches_list
})

# Close the driver when done
driver.quit()

# Save the DataFrame to a CSV file
df.to_csv('.\src\competitorsdummy.csv', index=False)

# Display the final DataFrame
print("FINAL RESULTS")
print("--------------------------")
print(df)
