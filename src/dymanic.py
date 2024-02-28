from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Initialize the web driver (ensure the driver path is correct for your setup)


# Lists to store data
names_list = []
competitors_list = []


driver = webdriver.Chrome()
url = "https://www.zomato.com/mumbai/melting-pot-juhu"
driver.get(url)
time.sleep(15)

# Name
name_elements = driver.find_elements(By.TAG_NAME, 'h1')
name = name_elements[0].text if name_elements else "N/A"
names_list.append(name)

a_tags = driver.find_elements(By.CSS_SELECTOR, '.sc-bnOsYM')
a_tags = [a_tag.get_attribute(
    "href") if a_tag else "N/A" for a_tag in a_tags]
a_tags.append(url)
competitors_list.append(a_tags)
driver.quit()

# Combine lists into DataFrame
df = pd.DataFrame({
    "Name": names_list,
    "list": competitors_list,
})

# Close the driver when done
driver.quit()

# Save the DataFrame to a CSV file
df.to_csv('.\src\competitorsname.csv', index=False)

# Display the final DataFrame
print("FINAL RESULTS")
print("--------------------------")
print(df)
