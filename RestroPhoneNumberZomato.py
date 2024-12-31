import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the WebDriver
driver = webdriver.Chrome()  # Replace with your WebDriver (e.g., ChromeDriver)
driver.get("https://www.zomato.com/jaipur/restaurants")  # Replace with your target website

# Wait for elements to load
wait = WebDriverWait(driver, 5)

# Set to track unique phone numbers
unique_phone_numbers = set()

# Data storage to avoid duplicates
unique_data = []
unique_identifiers = set()  # Set to track unique combinations of phone number and restaurant name

# Load existing data from the CSV file if it exists
try:
    with open("CSVs/zomato_data.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        existing_data = list(reader)  # Read all data into a list
        # Get the last serial number, skipping the header
        last_sno = max(int(row[0]) for row in existing_data[1:]) if len(existing_data) > 1 else 0
        
        # Populate unique_identifiers with existing data
        for row in existing_data[1:]:  # Skip header
            unique_identifiers.add((row[1], row[2]))  # (Phone No., Restaurant Name)
except FileNotFoundError:
    existing_data = []  # If the file doesn't exist, start with an empty list
    last_sno = 0  # Start from 0 if the file does not exist

# Initialize the serial number for new entries
sno = last_sno + 1

try:
    while True:  # Repeat until all buttons are processed
        # Locate all the buttons
        buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cRThYq")))

        for index in range(len(buttons)):
            try:
                # Re-locate the buttons in each loop to avoid stale element issues
                buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cRThYq")))

                # Get restaurant name, address, and link from the main page
                restaurant_name = buttons[index].find_element(By.CLASS_NAME, "sc-Ehqfj.bxOQva").text
                address = buttons[index].find_element(By.CLASS_NAME, "uIMEk").text
                link = buttons[index].find_element(By.CLASS_NAME, "kCiEKB").get_attribute("href")

                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView();", buttons[index])
                time.sleep(1)  # Optional delay for visual confirmation

                # Click the button
                buttons[index].click()

                # Wait for the new content to load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dIdAej")))  # Adjust locator

                # Scrape the phone number
                phone_no = driver.find_element(By.CLASS_NAME, "leEVAg").text

                # Check for duplicates using unique identifiers
                identifier = (phone_no, restaurant_name)  # Create a unique identifier
                if identifier not in unique_identifiers:
                    # Add identifier to the set
                    unique_identifiers.add(identifier)

                    # Store the unique data
                    unique_data.append([sno, phone_no, restaurant_name, address, link])
                    print(f"Row {sno} added: {restaurant_name}, {phone_no}, {address}, {link}")

                    # Increment the serial number
                    sno += 1

                # Navigate back
                driver.back()

                # Wait for the main page to reload
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cRThYq")))

            except Exception as e:
                print(f"Error processing button {index + 1}: {e}")
                continue

        # Optional: Break the loop if there's a finite number of buttons
        # break
        

finally:
    # Save the data to the CSV file
    with open("CSVs/zomato_data.csv", mode="a", newline="", encoding="utf-8") as file:  # Change mode to 'a'
        writer = csv.writer(file)
        # Write the header row only if the file was newly created
        if not existing_data:
            writer.writerow(["S.No.", "Phone No.", "Restaurant Name", "Address", "Link"])
        # Write unique rows
        writer.writerows(unique_data)
        print(f"Data appended to 'CSVs/zomato_data.csv'")

    # Close the browser
    driver.quit()
