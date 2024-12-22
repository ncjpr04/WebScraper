from bs4 import BeautifulSoup
import os

d = {'Title': [1, 2], 'Price': [3, 4], 'Link': [5, 6]}

for file in os.listdir("data"):
    with open(f"data/{file}","r") as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    t= soup.find("h2")
    title= t.get_text()
    break
print(soup.prettify())