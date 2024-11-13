import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.gsheets import get_google_sheet
import pandas as pd

gsheets_link = r"https://docs.google.com/spreadsheets/d/1h1z81KecxDBeBd8IjxKfdlAJ2Hx7eUvHRynml3aZF1Y/"
data = pd.DataFrame(get_google_sheet(gsheets_link))
print(data.head())