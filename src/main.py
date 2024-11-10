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

    # Get the user's choice for uploading the CSV file(Google Sheets or Upload CSV File)
    status = st.radio("How would you like to upload the CSV file?", ('Google Sheets', 'Upload CSV File'))

    # conditional statement
    if (status == 'Google Sheets'):
        df = google_sheet()

    else:
        df = upload_csv()


if __name__ == '__main__':
    main()