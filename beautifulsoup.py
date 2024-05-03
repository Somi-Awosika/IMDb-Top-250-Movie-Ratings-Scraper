
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time

def scrape_imdb_ratings(url, max_retries=3):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    
    # Retry mechanism
    for retry in range(max_retries):
        try:
            # Fetch the webpage
            driver.get(url)
            
            # Wait for the ratings to be visible
            wait = WebDriverWait(driver, 50)  # Maximum wait time of 50 seconds
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".lister-item-content .ratings-bar strong")))
            
            # Extract the page source
            html = driver.page_source
            
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            
            # Extract movie titles and ratings
            titles = [a.text.strip() for a in soup.select(".lister-item-content .lister-item-header a")]
            ratings = [float(span.text.strip()) for span in soup.select(".lister-item-content .ratings-bar strong")]
            
            # Close the WebDriver
            driver.quit()
            
            return titles, ratings
        
        except TimeoutException: # type: ignore
            if retry < max_retries - 1:
                print("TimeoutException occurred. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying
                continue
            else:
                print("Max retries reached. Unable to scrape data.")
                driver.quit()
                return None, None

# URL of IMDb's top-rated movies list
url = "https://www.imdb.com/chart/top"

# Scrape IMDb ratings
titles, ratings = scrape_imdb_ratings(url)

if titles and ratings:
    # Print the extracted data (for verification)
    print("Extracted Movie Titles:", titles[:10])
    print("Extracted Ratings:", ratings[:10])

    # Plot movie ratings as a vertical bar chart
    plt.figure(figsize=(12, 8))
    plt.bar(titles[:10], ratings[:10], color='skyblue')
    plt.xlabel('Movie')
    plt.ylabel('Rating')
    plt.title('Top 10 IMDb Movies by Rating')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No data retrieved. Unable to plot.")





