from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import csv

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Define the query and the CSV file for storing the data
query = "smartphone"
file = 0
idx=1
# Open a CSV file for writin
with open('CSVs/product_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['S no.', 'Title', 'Price', 'Product Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # Write the header to the CSV file
    writer.writeheader()

    for i in range(1, 5):
        # Open the Flipkart search results page
        driver.get(f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page={i}")
        
        # Find all product elemen
        elems = driver.find_elements(By.CLASS_NAME, "tUxRFH")
        print(f"Number of elements: {len(elems)}")
       
        for  elem in (elems):
            try:
                # Extract the product title
                title_elem = elem.find_element(By.CLASS_NAME, "KzDlHZ")
                title = title_elem.text if title_elem else "No title"
                
                # Extract the product link
                link_elem = elem.find_element(By.CLASS_NAME, "CGtC98")
                link = link_elem.get_attribute("href") if link_elem else "No link"
                
                # Extract the price
                price_elem = elem.find_element(By.CLASS_NAME, "_4b5DiR")
                price = price_elem.text if price_elem else "No price"
                
                # Write the data to the CSV file
                writer.writerow({'S no.': idx, 'Title': title, 'Price': price, 'Product Link': link})
                idx+=1
                # Save the HTML content for debugging
                d = elem.get_attribute("outerHTML")
                with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
                    f.write(d)
                    file += 1

            except Exception as e:
                print(f"Error processing product: {e}")
                continue

        # Add delay between requests to avoid being blocked
        time.sleep(5)

# Close the browser
driver.close()

print("Scraping completed and data saved to 'product_data.csv'.")
