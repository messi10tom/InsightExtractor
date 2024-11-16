# # src/main.py

# import sys
import os

# # Add the src directory to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import re
import streamlit as st
import pandas as pd
from io import StringIO
from utils.gsheets import get_google_sheet, update_google_sheet_from_df
from gspread.exceptions import NoValidUrlKeyFound
from llm.engine import (get_entity_from_ollama, 
                        preprocess_df_for_llm,
                        get_entity_from_gemini,
                        get_entity_chatgpt)
from selenium.common.exceptions import WebDriverException
from urllib3.exceptions import ProtocolError
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
            print('\n\nSuccesfully uploaded via computer\n\n')

        except UnicodeDecodeError:

            st.error("Invalid file format")
            return None
        
        except pd.errors.ParserError:

            st.error("Invalid file format")
            return None
        
        except Exception as e:

            st.error(f"An error occurred: {e}")
            return None
        
        # display the dataframe
        st.write(df)

        return df
    
    return None


def CSV_from_google_sheet() -> pd.DataFrame:
    
    # TODO: Multiple pages in google sheets

    # get the link of the google sheet
    with st.form("my_form"):
        link = st.text_input("Enter the link of the google sheet")
        st.form_submit_button("Submit")
    # get the google sheet data
    if link:
        try:
            df = pd.DataFrame(get_google_sheet(link))
            print('\n\nSuccesfully uploaded via GSheets\n\n')

            # display the dataframe
            st.write(df)
            return df, link
        except PermissionError:
            st.error('In sheets, change access "Restricted" to "Anyone with link"')
            return None
        
        except NoValidUrlKeyFound:
            st.error('Invalid URL')
            return None
        
        except Exception as e:

            st.error(f"An error occurred: {e}")
            return None


# Helper function to convert LLM output to a structured Dictionary
def LLM_out_to_dict(output: str) -> pd.DataFrame:
    out = pd.DataFrame(output)
    out = out.to_dict(orient='list')
    LLM_gen_entities = out.keys()
    return out, LLM_gen_entities

def Gemini_out_parser(output) -> pd.DataFrame:

    output = output.content
    # Extract JSON using regex to remove the markdown formatting
    json_string = re.search(r'```json\n({.*})\n```', output, re.DOTALL).group(1)

    # Load JSON to a dictionary
    data_dict = json.loads(json_string)

    # Convert "result" list to a DataFrame
    return pd.DataFrame(data_dict["result"])

def update_df(df: pd.DataFrame, 
              llm_entities: list,
              user_def_entities: list,
              ai_data: dict,
              idx:int) -> pd.DataFrame:
    
    for key in llm_entities:
        # Skip the 'Links' column or any user given data
        if key in user_def_entities:
            continue

        print(f'\n\n{'\n'.join(ai_data[key])}\n\n')

        # Update a cell in the new column
        df.at[idx, key] = '\n'.join(ai_data[key])
        print(f'\n\n{key}\n{df[key]}\n\n')
    return df

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

    model = st.radio("Select the model", ('Gemini', 'ChatGPT', 'Ollama'))
    df = None

    # Get the user's choice for uploading the CSV file(Google Sheets or Upload CSV File)
    status = st.radio("How would you like to upload the CSV file?", ('Google Sheets', 'Upload CSV File'))
    
    # conditional statement
    if (status == 'Upload CSV File'):
        df = upload_csv_from_device()

    else:
        try:

            df, gsheet_link = CSV_from_google_sheet()

        except TypeError:
            pass

        except Exception as e:
            st.write(f"Something gone wrong try again. {e}")

    # Check if the DataFrame is not empty
    if df is not None:
        # Prompt the user to enter a prompt.
        # This prompt will be used to perform a similarity search and RAG (Retrieval-Augmented Generation) pipeline
        # to collect relevant data from the scraped content.
        # The collected data will be based on the entities specified in the first row of the CSV file, excluding the 'Links' column.
        st.write('You can use placeholders to specify the entities you want to collect from the websites.')
        st.write('For example, "I need the Email of the {company} and all the names you could find from the {company}."')
        st.write('The placeholders should match the data entities in the first row of the CSV file.')
        st.write('{company} will be replaced by company information from the CSV file.')
        print('succesfully_uploaded')
        user_def_entities = df.columns.tolist()
        
        with st.form('key 2'):
           user_prompt = st.text_area("Enter the Prompt")
           st.form_submit_button('Submit')

        st.write(f"User Prompt: {user_prompt}")

        if user_prompt.strip():
             
            print(f'\n\n{user_prompt}\n\n')
            
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

            # Create a new column to store the formatted text
            # Helper function: create placeholder for user to enter
            def replace_placeholders(row, template):
                return template.format(**row)

            # Apply the function to each row in the DataFrame
            df['formatted'] = df.apply(lambda row: replace_placeholders(row, user_prompt), axis=1)
            formatted_user_prompt = df['formatted'].tolist()

            # Scrape the links
            for idx, (link, prompt) in enumerate(zip(links, formatted_user_prompt)):
                try:

                    progress_placeholder.text(f'Submitting file and scraping URL {link}')
                    print(f'\033[91mscraping from {link}\033[0m')
                    html = scrape(link)

                except WebDriverException as e:
                    if "Account is suspended" in str(e):
                        st.write('Your https://brightdata.com/ service over.')

                    elif "Message: Zone not found" in str(e):
                        st.write('Please provide Bright Data Zone ID in the .env file.')

                    else:
                        print(e)
                        st.write(f'Invalid URL({link}) found in the CSV file. Please check the URLs.')

                    html = [str(e)]
                except ProtocolError  as e:

                    st.write(f"Network error({link}). Please try later...")
                    html = [str(e)]
                
                except Exception as e:

                    print(f'Error: {e}.')
                    html = [str(e)]
                
                if type(html) is not list:
                    
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
                    try:
                        if model == 'ChatGPT':

                            entity = get_entity_chatgpt(text, csv_data, prompt)

                        elif model == 'Gemini':
                                
                            entity = get_entity_from_gemini(text, csv_data, prompt)

                        else:

                            entity = get_entity_from_ollama(text, csv_data, prompt)

                        print(f'\n\n{entity}\n\n')

                    except SyntaxError as e:
                        #  SyntaxError: invalid syntax 
                        st.write(f'Error in AI generation({link}).')
                        entity = str(e)
                    
                    except Exception as e:

                        entity = str(e)
                    
                    if entity is None:

                        entity = ['Error in AI generation. Please try again.']
                        progress_placeholder.text(f'Failed AI generation from the URL {link} due to Error in AI generation.')
                        print(f'Error in scraping {link}. Please check the URL.')

                    elif type(entity) is str:

                        progress_placeholder.text(f'Failed AI generation from the URL {link} due to {entity[0]}')
                        print(f'Error in scraping {link}. Please check the URL.')
                        
                    else:
                        print('successfully AI generated')
                        print(entity)


                        # Convert the LLM output to a structured dictionary
                        entity, LLM_gen_entities = LLM_out_to_dict(entity)
                        print(f'\n\n{entity}\n\n')

                    
                        # Update the DataFrame with the generated entities
                        df = update_df(df, LLM_gen_entities, user_def_entities, entity, idx)

                        print("\n\nstructured output:\n\n", LLM_gen_entities)
                        # for key in LLM_gen_entities:

                        #     # Skip the 'Links' column or any user given datas
                        #     if key in df.columns and not df[key].isnull().all():
                        #         continue

                        #     # Check if the column exists, if not, create it
                        #     if key not in df.columns:
                        #         df[key] = None

                        #     print(Back.BLUE + f'\n\nhi{key}\n{df[key]}\n\n' + Style.RESET_ALL)
                        #     print(Back.GREEN + f'\n\nhi{'\n'.join(entity[key])}\n\n' + Style.RESET_ALL)
                            
                        #     # Update a cell in the new column
                        #     df.at[idx, key] = '\n'.join(entity[key])
                        #     print(Back.BLUE + f'\n\n{key}\n{df[key]}\n\n' + Style.RESET_ALL)

                else:

                    progress_placeholder.text(f'Failed webscraping from the URL {link} due to {html[0]}')
                    print(f'Error in scraping {link}. Please check the URL.')
              
                

            # Display the updated DataFrame
            df.drop(columns=['formatted'], inplace=True)
            st.write("Updated DataFrame")
            st.write(df)

            progress_placeholder.text('Process completed successfully.')

            # Save the updated DataFrame to a CSV file
            # Convert DataFrame to CSV
            csv = df.to_csv(index=False)
            csv_bytes = StringIO(csv).getvalue().encode('utf-8')

            # Download button
            succes = st.download_button(
                                    label="Download CSV",
                                    data=csv_bytes,
                                    file_name='output.csv',
                                    mime='text/csv',
                                )
            if succes:
                print('succesfully downloaded')
                del text, csv_data, prompt, formatted_user_prompt, links, link, html
                os.remove("temp_credentials.json")
                st.stop()
    
    else:
        st.write("Please wait...")
                   




if __name__ == '__main__':
    main()