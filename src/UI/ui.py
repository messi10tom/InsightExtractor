import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


# import the streamlit library
import streamlit as st
from src.utils.gsheets import get_google_sheet
from gspread.exceptions import NoValidUrlKeyFound
import pandas as pd


def upload_csv() -> pd.DataFrame:
    # get the uploaded file
    uploaded_files = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=False
    )

    # TODO: Add multiple file upload

    # for uploaded_file in uploaded_files:
    #     bytes_data = uploaded_file.read()
    #     st.write("filename:", uploaded_file.name)
    #     st.write(bytes_data)


    if uploaded_files is not None:
        # convert the uploaded file to a pandas dataframe
        try:

            df = pd.read_csv(uploaded_files)

        except UnicodeDecodeError:
            st.error("Invalid file format")
            return None
        
        except pd.errors.ParserError:
            st.error("Invalid file format")
            return None
        # display the dataframe
        st.write(df)

        return df
    
    return None

def google_sheet() -> pd.DataFrame:
    
    # TODO: Multiple pages in google sheets

    # get the link of the google sheet
    link = st.text_input("Enter the link of the google sheet")
    if st.button("Get Google Sheet"):
        # get the google sheet data
        try:
            df = get_google_sheet(link)
        except PermissionError:
            st.error('In sheets, change access "Restricted" to "Anyone with link"')
            return None
        
        except NoValidUrlKeyFound:
            st.error('Invalid URL')
            return None

        # display the dataframe
        st.write(df)
        return df



