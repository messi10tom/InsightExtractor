import os
from dotenv import load_dotenv
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# TODO: Document this function
AUTH = os.getenv('BD_AUTH')
if not AUTH:
    raise ValueError("No BD_AUTH environment variable set")

SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

def scrape(link: str) -> str: 
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(link)

        print('Navigated! Scraping page content...')
        html = driver.page_source
    
    return html

def extract_text_from_html(html: str) -> str:

    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    
    return text
