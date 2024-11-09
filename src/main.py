import streamlit as st
from src.UI.ui import upload_csv, google_sheet

# Welcome to InsightExtractor
st.title('Welcome to InsightExtractor')

# Get the user's choice for uploading the CSV file(Google Sheets or Upload CSV File)
status = st.radio("How would you like to upload the CSV file?", ('Google Sheets', 'Upload CSV File'))

# conditional statement
if (status == 'Google Sheets'):
    df = google_sheet()

else:
    df = upload_csv()