from bs4 import BeautifulSoup
import os

# Dictionary to store extracted data
d = {'Title': [], 'Price': [], 'Link': []}

# Ensure the 'data' directory exists and contains files
if not os.path.exists("data") or not os.listdir("data"):
    print("The 'data' directory is empty or does not exist.")
else:
    for file in os.listdir("data"):
        try:
            # Open and read each file
            with open(f"data/{file}", "r", encoding="utf-8") as f:
                html_doc = f.read()

            # Parse the HTML content
            soup = BeautifulSoup(html_doc, 'html.parser')

            # Extract title (h2 tag)
            t = soup.find("h2")
            title = t.get_text() if t else "No title found"
            d['Title'].append(title)

            # Print the prettified HTML for debugging (optional)
            print(f"Contents of file {file}:")
            print(soup.prettify())

        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Print the collected data
print("\nExtracted Data:")
print(d)
