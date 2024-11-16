import os
from dotenv import load_dotenv

import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe

load_dotenv()
CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def get_google_sheet(link: str):
    """
    
    Get the google sheet data
    Args:
        link (str): the link of the google sheet
    Returns:
        the data of the google sheet

    """

    scope = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_file(CREDENTIALS, scopes=scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(link).sheet1
    data = sheet.get_all_records()

    return data

def update_google_sheet_from_df(link: str, df):
    """
    Update a Google Sheet with the data from a pandas DataFrame.
    
    Args:
        spreadsheet_id (str): The ID of the Google Sheet.
        worksheet_name (str): The name of the worksheet to update.
        df (pd.DataFrame): The pandas DataFrame containing the data to update.
    """
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(CREDENTIALS, scopes=scope)
    client = gspread.authorize(creds)
    
    # Open the Google Sheet
    sheet = client.open_by_url(link)
    
    # Select the worksheet
    worksheet = sheet.sheet1
    
    # Clear the existing content in the worksheet
    worksheet.clear()
    
    # Update the worksheet with the DataFrame
    set_with_dataframe(worksheet, df)
    
    print(f"Updated Google Sheet '{link}' in worksheet sheet1 with DataFrame data.")
    
    return True