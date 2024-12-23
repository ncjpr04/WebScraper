from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize WebDriver
driver = webdriver.Chrome()  # Use the WebDriver for your browser

try:
    # Open Monkeytype
    driver.get("https://monkeytype.com")
    print("Opened Monkeytype.")

    # Wait for the page to load
    time.sleep(5)  # Adjust this based on your internet speed

    # Find the typing input field
    typing_input = driver.find_element(By.ID, "wordsInput")

    # Find the text that needs to be typed
    words = driver.find_elements(By.CLASS_NAME, "word")
    words_text = " ".join([word.text for word in words])

    # Wait until the input field is ready for typing
    while not typing_input.is_enabled():
        time.sleep(1)

    # Type the words automatically
    for char in words_text:
        typing_input.send_keys(char)  # Simulate typing each character
        time.sleep(0.01)  # Adjust typing speed by modifying the sleep time

    # Once typing is done, print the results
    print("Typing completed.")
    for word in words:
        word_status = "active" if "active" in word.get_attribute("class") else "typed"
        print(f"Word: {word.text} | Status: {word_status}")

    # Wait for 3 seconds after typing is complete
    time.sleep(3)
finally:
    # Wait for the user to press 'q' to close the WebDriver
    q = input("Results displayed. Press 'q' and hit Enter to close the WebDriver...")

    if q == 'q':
        driver.quit()
        print("WebDriver closed.")
