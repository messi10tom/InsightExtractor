# src/main.py

import streamlit as st
from UI.ui import upload_csv, google_sheet

def main():
    # Welcome to InsightExtractor
    st.title('Welcome to InsightExtractor')

    # Get the user's choice for uploading the CSV file(Google Sheets or Upload CSV File)
    status = st.radio("How would you like to upload the CSV file?", ('Google Sheets', 'Upload CSV File'))

    # conditional statement
    if (status == 'Google Sheets'):
        df = google_sheet()

    else:
        df = upload_csv()

if __name__ == '__main__':
    main()