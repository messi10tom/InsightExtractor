# import the streamlit library
import streamlit as st
import pandas as pd


# Welcome to InsightExtractor
st.title('Welcome to InsightExtractor')

import streamlit as st

uploaded_files = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=False
)

# TODO: Add multiple file upload

# for uploaded_file in uploaded_files:
#     bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)
#     st.write(bytes_data)

