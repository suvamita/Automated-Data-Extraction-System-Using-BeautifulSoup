import requests
from bs4 import BeautifulSoup
import re

def scrape_movie_titles(url):
    """
    Function to scrape movie titles from subslikescript.com
    """
    movie_titles = []
    page_num = 1
    
    while True:
        # Construct the URL for the current page
        page_url = f"{url}/page/{page_num}" if page_num > 1 else url
        
        # Send a GET request to the current page URL
        response = requests.get(page_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all <a> tags within <ul class="scripts-list">
            movie_links = soup.find('ul', class_='scripts-list').find_all('a')
            
            # Extract movie titles from each <a> tag
            page_titles = [link.get_text(strip=True) for link in movie_links]
            movie_titles.extend(page_titles)
            
            # Check if there's a next page link
            next_page_link = soup.find('a', class_='next page-numbers')
            if not next_page_link:
                break  # Exit the loop if no next page is found
            
            # Increment page number for the next iteration
            page_num += 1
        else:
            print(f"Failed to retrieve page {page_url}. Status code: {response.status_code}")
            break
    
    return movie_titles

# URL of the main page with movie titles
url = 'https://subslikescript.com/movies_letter-A?page=1'

# Scrape movie titles with pagination
movie_titles = scrape_movie_titles(url)

# Sanitize movie titles by removing text in parentheses (usually the year)
sanitized_titles = [re.sub(r'\s*\([^)]*\)', '', title) for title in movie_titles]

# Print the sanitized movie titles
for title in sanitized_titles:
    print(title)
