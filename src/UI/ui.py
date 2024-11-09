# import the streamlit library
import streamlit as st
from src.utils.gsheets import get_google_sheet
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
        df = pd.read_csv(uploaded_files)
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
        df = get_google_sheet(link)
        # display the dataframe
        st.write(df)
        return df



