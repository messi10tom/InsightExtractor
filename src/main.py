# src/main.py

import streamlit as st
import pandas as pd
from UI.ui import upload_csv, google_sheet
from scraper.webscraper import scrape, extract_text_from_html

def main():
    # Welcome to InsightExtractor
    st.title('Welcome to InsightExtractor')
    sample_df = pd.read_csv('./sample.csv')
    st.write('Here is a sample CSV file')
    st.write(sample_df)
    st.write('The CSV file should contain a column named "Links" with the URLs of the webpages you want to scrape.')
    st.write('First row contains only "Links" and data entities that you want to scrape should be in the subsequent rows.')

    # Get the user's choice for uploading the CSV file(Google Sheets or Upload CSV File)
    status = st.radio("How would you like to upload the CSV file?", ('Google Sheets', 'Upload CSV File'))
    
    # conditional statement
    if (status == 'Google Sheets'):
        df = google_sheet()

    else:
        df = upload_csv()

    # Check if the DataFrame is not empty
    if df is not None and not df.empty:
        # TODO: Error management
        # Check if the DataFrame contains a 'Links' column
        
        if 'Links' not in df.columns:
            st.error('The CSV file does not contain a column named "Links"')
            return
        
        links = df['Links'].tolist()

        # Scrape the links
        for link in links:
            html = scrape(link)
            text = extract_text_from_html(html)
            print(text)



if __name__ == '__main__':
    main()