from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
query ="smartphone"
page=1
driver.get(f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page={page}")
elems = driver.find_elements(By.CLASS_NAME,"col-7-12" )
print("Number of elements:"+{len(elems)})
for elem in elems:
    print(elem.text)
time.sleep(5)
driver.close()