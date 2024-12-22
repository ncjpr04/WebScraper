from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
query ="smartphone"
file=0
for i in range(1,5):
    driver.get(f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page={i}")
    elems = driver.find_elements(By.CLASS_NAME,"col-7-12" )
    print(f"Number of elements:{len(elems)}")
    for elem in elems:
        # print(elem.text)
        d=elem.get_attribute("outerHTML")
        with open(f"data/{query}_{file}.html","w") as f:
            f.write(d)
            file+=1
    time.sleep(5)

driver.close()
