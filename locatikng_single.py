from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
query ="smartphone"
driver.get(f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off")
elem = driver.find_element(By.CLASS_NAME,"col-7-12" )
print(elem.get_attribute("outerHTML"))
time.sleep(5)
driver.close()