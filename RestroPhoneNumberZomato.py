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

try:
    sno = 1  # Serial number counter

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

                # Check for duplicates
                if phone_no not in unique_phone_numbers:
                    # Add phone number to the set
                    unique_phone_numbers.add(phone_no)

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
    with open("CSVs/zomato_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["S.No.", "Phone No.", "Restaurant Name", "Address", "Link"])
        # Write unique rows
        writer.writerows(unique_data)
        print(f"Data saved to 'CSVs/zomato_data.csv'")

    # Close the browser
    driver.quit()
