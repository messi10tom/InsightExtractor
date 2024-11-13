# InsightExtractor

![InsightExtractor Banner](./doc/banner.png)

InsightExtractor is an AI-powered tool for automated data retrieval. Connect CSVs or Google Sheets, define queries, and extract structured insights via web search and LLMs. Features include customizable prompts, API integration, and an intuitive dashboard for data export.

## Features

- **Automated Data Retrieval**: Seamlessly connect CSVs or Google Sheets and extract data.
- **Customizable Prompts**: Define queries and prompts to tailor the data extraction process.
- **Web Scraping**: Scrape web data and integrate it with your structured data.
- **LLM Integration**: Utilize Language Models to process and extract insights from the data.
- **Intuitive Dashboard**: User-friendly interface for managing data and exporting results.
- **API Integration**: Easily integrate with other tools and services via APIs.

## Installation

To install InsightExtractor, follow these steps:

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/messi10tom/InsightExtractor.git
    cd InsightExtractor
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:
    - Create a `.env` file in the root directory and add your credentials:
    
    ```env
    - **Create BD_AUTH Token**:
        1. **Visit Bright Data**:
            - Go to [Bright Data](https://brightdata.com/).
        2. **Access the Dashboard**:
            - In the dashboard, choose "Scraping Browser" from the "Add" dropdown menu.
        3. **Name Your Scraping Browser**:
            - Name your scraping browser something like "InsightExtractor".
        4. **Create the Scraping Browser**:
            - Click the "Add" button to create the Scraping Browser.
        5. **Navigate to Playground**:
            - In your Scraping Browser, go to "Playground".
        6. **Toggle to Code Examples**:
            - Toggle "Playground" to "Code Examples".
        7. **Select Python, Selenium**:
            - In the "Run example script" snippet, choose "Python, Selenium".
        8. **Copy the AUTH Key**:
            - Copy the AUTH key provided in the example script.
        9. **Update .env File**:
            - Paste the AUTH key into the `BD_AUTH` field in your `.env` file.
    - **Create Google Application Credentials**:
        1. **Visit Google Cloud Console**:
            - Go to [Google Cloud Console](https://console.cloud.google.com/).
        2. **Select Google Account**:
            - Choose the appropriate Google account.
        3. **Create a Project**:
            - In the top menu, select the project list and create a new project.
        4. **Select the Project**:
            - Choose the newly created project.
        5. **Navigate to API & Services**:
            - Search for "API & Services" and select "Enabled API & Services".
        6. **Enable Google Sheets API**:
            - Click on "ENABLED API & SERVICES" and search for Google Sheets API.
        7. **Create Credentials**:
            - Click on "Create Credentials" and fill out the required forms.
        8. **Set Service Account Role**:
            - While filling out "Grant this service account access to projects", set the role to Editor.
        9. **Generate JSON Key**:
            - Go to "Credentials", then "Keys", and select "ADD KEYS".
            - Choose "Create New Key" and select "JSON".
        10. **Download and Move Key**:
            - Download the JSON key file and move it to the project directory.
        11. **Update .env File**:
            - Copy the file path and paste it into the `GOOGLE_APPLICATION_CREDENTIALS` field in your `.env` file.
            
    BD_AUTH=your_auth_details
    GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
    ```

4. **Run the Application**:
    ```sh
    streamlit run src/main.py
    ```

## Usage

1. **Upload CSV or Google Sheets**:
    - Choose to upload a CSV file or connect to a Google Sheet.
    - Ensure the CSV file contains a column named "Links" with the URLs of the webpages you want to scrape.

2. **Define Your Query**:
    - Enter a prompt to define what data you want to extract.

3. **Extract Data**:
    - The tool will scrape the web data, process it using LLMs, and present the extracted insights.

4. **Export Results**:
    - Download the results as a CSV file for further analysis.

## Example

Here is an example of how to use InsightExtractor:

1. **Sample CSV File**:
    ```csv
    Links,company
    example1.com,company_1
    example2.com,company_2
    ```

2. **User Prompt**:
    ```
    Extract the names, emails, and companies of the professionals mentioned in the text.
    ```
  ```

## Contributing

We welcome contributions to InsightExtractor! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Selenium](https://www.selenium.dev/)
