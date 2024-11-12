# src/main.py

# import sys
# import os

# # Add the src directory to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
from io import StringIO
from utils.gsheets import get_google_sheet
from gspread.exceptions import NoValidUrlKeyFound
from llm.engine import get_entity_from_ollama, preprocess_df_for_llm
from selenium.common.exceptions import WebDriverException
from scraper.webscraper import scrape, extract_text_from_html



def upload_csv_from_device() -> pd.DataFrame:
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


def CSV_from_google_sheet() -> pd.DataFrame:
    
    # TODO: Multiple pages in google sheets
    # TODO: Update current Google Sheet using the Google Sheets API

    # get the link of the google sheet
    link = st.text_input("Enter the link of the google sheet")
    if st.button("Get Google Sheet"):
        # get the google sheet data
        try:
            df = pd.DataFrame(get_google_sheet(link))
        except PermissionError:
            st.error('In sheets, change access "Restricted" to "Anyone with link"')
            return None
        
        except NoValidUrlKeyFound:
            st.error('Invalid URL')
            return None

        # display the dataframe
        st.write(df)
        return df

# Helper function to convert LLM output to a structured Dictionary
def LLM_out_to_dict(output: str) -> pd.DataFrame:
    out = pd.DataFrame(output)
    out = out.to_dict(orient='list')
    LLM_gen_entities = out.keys()
    return out, LLM_gen_entities


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
        df = CSV_from_google_sheet()

    else:
        df = upload_csv_from_device()

    # Check if the DataFrame is not empty
    if df is not None and not df.empty:
        # Prompt the user to enter a prompt.
        # This prompt will be used to perform a similarity search and RAG (Retrieval-Augmented Generation) pipeline
        # to collect relevant data from the scraped content.
        # The collected data will be based on the entities specified in the first row of the CSV file, excluding the 'Links' column.
        user_prompt = st.text_input("Enter the Prompt")
        if st.button('Submit'):
            # TODO: Error management
            # TODO: Add a radio to select different models
            # Check if the DataFrame contains a 'Links' column

            # Create a placeholder for progress messages

            # | Links        | company   |
            # |--------------|-----------|
            # | example1.com | company_1 |
            # | example2.com | company_2 |

            progress_placeholder = st.empty()

            if 'Links' not in df.columns:
                st.error('The CSV file does not contain a column named "Links"')
                return
        
            links = df['Links'].tolist()

            # Scrape the links
            for idx, link in enumerate(links):
                try:

                    progress_placeholder.text(f'Submitting file and scraping URL {idx + 1}/{len(links)}...')
                    html = scrape(link)

                except WebDriverException:
                    st.error(f'Invalid URL({link}) found in the CSV file. Please check the URLs and try again.')

                    return
                print(f'successfully scraped from {link}')

            
                text = extract_text_from_html(html)
                
                print(f'successfully extracted\n{text[:200]}')

                # Get the data from csv file (header + idx row)
                # |    Links        |   company   |
                # |-----------------|-------------|
                # | example_idx.com | company_idx |
                # |-----------------|-------------|
                #                   |
                #                   |
                #                   v
                # Links company example_idx.com company_idx
              

                csv_data = pd.concat([df.head(0), df.iloc[[idx]]])
                csv_data = preprocess_df_for_llm(csv_data)
                progress_placeholder.text('Sending text to LLM...')
                
                # get_entity_from_ollama(web_data: str, data_entity: list, user_prompt: str) -> str:
                entity = get_entity_from_ollama(text, csv_data, user_prompt)
                if entity is None:
                    st.error('Error in AI generation. Please try again.')
                    return
                else:
                    print('successfully AI generated')
                print(entity)


                # Convert the LLM output to a structured dictionary
                entity, LLM_gen_entities = LLM_out_to_dict(entity)

                for key in LLM_gen_entities:

                    # Check if the column exists, if not, create it
                    if key not in df.columns:
                        df[key] = None

                    # Update a cell in the new column
                    df.at[idx, key] = '\n'.join(entity[key]) 

            # Display the updated DataFrame
            st.write("Updated DataFrame")
            st.write(df)

            progress_placeholder.text('Process completed successfully.')

            # Save the updated DataFrame to a CSV file
            # Convert DataFrame to CSV
            csv = df.to_csv(index=False)
            csv_bytes = StringIO(csv).getvalue().encode('utf-8')

            # Download button
            st.download_button(
                label="Download CSV",
                data=csv_bytes,
                file_name='output.csv',
                mime='text/csv',
            )



if __name__ == '__main__':
    main()