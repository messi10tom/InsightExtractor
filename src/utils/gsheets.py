import os
from dotenv import load_dotenv

import gspread
from google.oauth2.service_account import Credentials

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

