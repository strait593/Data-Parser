import requests
from bs4 import BeautifulSoup
import lxml
from urllib.parse import urljoin
import urllib
import re
from re import compile
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_authors import Base_Authors, Author
from database_quotes import Base_Quotes, Quote
from separate_tables import create_authors, create_quotes

#Things to steal from site
#   Authors and their biography
#   quotes

#obtain the list of links for each author
def fetch_links():
    url = "https://quotes.toscrape.com/"
    html = requests.get(url)

    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'lxml')
        print("---Loaded the html file---")
    else:
        print("An error has ocurred.")

    links = soup.find_all("a", href=re.compile(r"/author"))
    
    author_links = []

    for link in links:
        url = link.get("href")

        if url:
            author_links.append(url)

    #obtain unique list of links
    return list(set(author_links))

def parse_authors_data(base_url="http://quotes.toscrape.com"):
    scraped_data = []
    obtained_links = fetch_links()
    
    print(f"--- Starting the jump through {len(obtained_links)} links ---")

    for link in obtained_links:
        try:
            #create the bridge between the pages
            abs_link = urllib.parse.urljoin(base_url, link)
            print(f"Jumping to: {abs_link}")

            #make the request
            response = requests.get(abs_link, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            #extract the data
            name = soup.find('h3', class_="author-title").text.strip()
            born_date = soup.find("span", class_="author-born-date").text.strip()
            born_location = soup.find("span", class_="author-born-location").text.strip()
            description = soup.find("div", class_="author-description").text.strip()

            author_entry = {
                'Fullname': name,
                'Date of Birth': born_date,
                'Born location': born_location,
                'Description': description
            }

            scraped_data.append(author_entry)
            print(f"Successfully scraped: {name}")

            # create a short pause(aparently you can get blocked by the provider for aggressive and fast requests)
            time.sleep(0.5)

        except Exception as e:
            print(f"Failed to jump into {link}: {e}")
            continue

    return scraped_data


def parse_quotes(base_url="https://quotes.toscrape.com/"):
    current_url = base_url
    all_quotes = []

    while current_url:
        print(f"--- Scraping: {current_url} ---")
        response = requests.get(current_url)

        if response.status_code != 200:
            print("An error has occurred reaching the page.")
            break

        soup = BeautifulSoup(response.text, 'lxml')

        # 1. Identify all quote containers on the current page
        quote_elements = soup.find_all("div", class_="quote")

        for element in quote_elements:
            # extract text from  the each quote container
            text = element.find("span", class_="text").text.strip()
            author = element.find("small", class_="author").text.strip()

            # Ta
            tags = [tag.text for tag in element.find_all("a", class_="tag")]

            quote_entry = {
                "quote": text,
                "author": author,
                "tags": tags
            }
            all_quotes.append(quote_entry)

        #find the "next" button
        next_btn = soup.find("li", class_="next")
        if next_btn:
            #extract the path
            relative_path = next_btn.find("a")["href"]
            #join it with the base URL to get the full address
            current_url = urllib.parse.urljoin(base_url, relative_path)
        else:
            #if we run out of buttons to press, the script stops
            current_url = None

    return all_quotes

print(f"List of obtained links: {fetch_links()}")
print(f"List of all the parsed data: {parse_authors_data()}")
print(f"List of all the quotes obtained: {parse_quotes()}")

if __name__ == "__main__":

    print("--- Scraping Quotes ---")
    quotes_data = parse_quotes()

    print("--- Scraping Authors ---")
    authors_info = parse_authors_data()

    engine = create_engine("sqlite:///gathered.db")

    Base_Authors.metadata.create_all(engine)
    Base_Quotes.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        for entry in authors_info:
            author_obj = Author(
                fullname=entry["Fullname"],
                date_of_birth=entry['Date of Birth'],
                born_location=entry["Born location"],
                description=entry["Description"]
            )
            session.add(author_obj)


        for text in quotes_data:

            tag_string = ", ".join(text['tags'])

            quote_obj = Quote(
                quote=text['quote'],
                author=text['author'],
                tags=tag_string
            )
            session.add(quote_obj)

        session.commit()
        print(f"\n--- Done: Saved {len(authors_info)} authors and {len(quotes_data)} quotes ---")

    except Exception as e:
        print(f"An error occurred during DB insertion: {e}")
        session.rollback()
        
    finally:
        create_quotes()
        create_authors()
        session.close()