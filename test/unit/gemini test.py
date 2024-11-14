import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.llm.engine import get_entity_from_gemini, preprocess_df_for_llm
from src.scraper.webscraper import scrape, extract_text_from_html
from src.main import LLM_out_to_dict, Gemini_out_parser
import pandas as pd


user_prompt = "find email from the {company} and also name of the workers if listed in the webpage I need the output in a appealing easy manner. you should only take name and email from the website"
df = pd.read_csv("./test/data/test data.csv")
links = df["Links"]

# Create a new column to store the formatted text
# Helper function: create placeholder for user to enter
def replace_placeholders(row, template):
    return template.format(**row)

# Apply the function to each row in the DataFrame
df['formatted'] = df.apply(lambda row: replace_placeholders(row, user_prompt), axis=1)
formatted_user_prompt = df['formatted'].tolist()

for idx, (link, prompt) in enumerate(zip(links, formatted_user_prompt)):

    print(f"Processing link: {link}")

    web_data = extract_text_from_html(scrape(link))

    csv_data = pd.concat([df.head(0), df.iloc[[idx]]])
    csv_data = preprocess_df_for_llm(csv_data)

    response = get_entity_from_gemini(web_data, csv_data, prompt)
    response = Gemini_out_parser(response).to_dict(orient='list')
    # Convert the LLM output to a structured dictionary
 
    for key in response.keys():

        # Skip the 'Links' column or any user given datas
        if key in df.columns and not df[key].isnull().all():
            continue

        # Check if the column exists, if not, create it
        if key not in df.columns:
            df[key] = None

        # Update a cell in the new column
        df.at[idx, key] = '\n'.join(response[key])

df.to_csv("./test/data/test data output.csv", index=False)
# TODO: write sript
# TODO: write test web app