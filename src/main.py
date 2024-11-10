# src/main.py

import streamlit as st
import pandas as pd
from UI.ui import upload_csv, google_sheet
from llm.engine import get_entity_from_ollama
from selenium.common.exceptions import WebDriverException
from scraper.webscraper import scrape, extract_text_from_html

def main():
    """
    Main function to run the InsightExtractor application.
    This function performs the following steps:
    1. Displays a welcome title and sample CSV file.
    2. Prompts the user to choose between uploading a CSV file via Google Sheets or direct upload.
    3. Reads the CSV file based on the user's choice.
    4. Checks if the DataFrame is not empty and contains a 'Links' column.
    5. Prompts the user to enter a prompt to understand what to collect from the websites listed.
    6. Scrapes the links provided in the 'Links' column of the CSV file.
    7. Extracts and prints the text from the HTML content of each link.
    Note:
    - The CSV file must contain a 'Links' column with the URLs to scrape.
    - The first row of the CSV file should contain only "Links" and data entities to scrape.
    - Error management is included to handle invalid URLs and missing 'Links' column.
    """
    # Welcome to InsightExtractor
    st.title('Welcome to InsightExtractor')
    sample_df = pd.read_csv('./sample.csv')
    st.write('Here is a sample CSV file')
    st.write(sample_df)
    st.write("Ensure your CSV file has a 'Links' column with the URLs to scrape.")
    st.write('First row contains only "Links" and data entities that you want to scrape.')

    # Get the user's choice for uploading the CSV file(Google Sheets or Upload CSV File)
    status = st.radio("How would you like to upload the CSV file?", ('Google Sheets', 'Upload CSV File'))
    
    # conditional statement
    if (status == 'Google Sheets'):
        df = google_sheet()

    else:
        df = upload_csv()

    # Check if the DataFrame is not empty
    if df is not None and not df.empty:
        # Prompt the user to enter a prompt.
        # This prompt will be used to perform a similarity search and RAG (Retrieval-Augmented Generation) pipeline
        # to collect relevant data from the scraped content.
        # The collected data will be based on the entities specified in the first row of the CSV file, excluding the 'Links' column.
        user_prompt = st.text_input("Enter the Prompt")
        if st.button('Submit'):
            print(user_prompt)

        # TODO: Error management
        # Check if the DataFrame contains a 'Links' column

        if 'Links' not in df.columns:
            st.error('The CSV file does not contain a column named "Links"')
            return
        
        links = df['Links'].tolist()

        # Scrape the links
        for link in links:
            try:

                html = scrape(link)

            except WebDriverException:
                st.error('Invalid URL found in the CSV file. Please check the URLs and try again.')

                return
            print('successfully scraped')
            text = extract_text_from_html(html)
            entity = get_entity_from_ollama(text, df.columns[1:], user_prompt)
            st.write(entity)



if __name__ == '__main__':
    main()