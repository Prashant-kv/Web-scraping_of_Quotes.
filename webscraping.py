from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

def main():   
    url = "http://quotes.toscrape.com"

    current_url = url
    all_data = []

    while current_url:
        response = requests.get(current_url)

        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully retrieved the page")
        else:
            print(f"Failed to retrieve the page with status code: {response.status_code}")
            return

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        quotes = soup.find_all("span", class_="text")
        authors = soup.find_all("small", class_="author")          #print(quote.attrs)  # It will give the attribute of the tag
                                                                   #print(quote.name)   # It will give the tag name
        data = []                                                  #print(quote.text)   # It will give the text or content of the tag 
        for quote, author in zip(quotes, authors):
            data.append({
                "Quote": quote.text,
                "Author": author.text
            })                                                           
        
        
        all_data.extend(data)

        next_button = soup.find("li", class_="next")

        if next_button:
            # Find the link for the next page
            next_page_link = next_button.find("a")["href"]
            current_url = url+next_page_link 
            print(current_url)
        else:
            current_url = None 
    save_file(all_data)

def save_file(all_data, filename="quotes.xlsx"):
    df = pd.DataFrame(all_data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

 
if __name__ == "__main__":
    main()
