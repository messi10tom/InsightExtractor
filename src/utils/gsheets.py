import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

def get_google_sheet(link: str) -> pd.DataFrame:
    """
    
    Get the google sheet data
    Args:
        link (str): the link of the google sheet
    Returns:
        pd.DataFrame: the data of the google sheet

    """

    scope = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open(link).sheet1
    data = sheet.get_all_records()

    return pd.DataFrame(data)

