# InsightExtractor
[![GitHub issues](https://img.shields.io/github/issues/messi10tom/InsightExtractor)](https://github.com/messi10tom/InsightExtractor/issues)
[![GitHub forks](https://img.shields.io/github/forks/messi10tom/InsightExtractor)](https://github.com/messi10tom/InsightExtractor/network)
[![GitHub stars](https://img.shields.io/github/stars/messi10tom/InsightExtractor)](https://github.com/messi10tom/InsightExtractor/stargazers)
[![GitHub license](https://img.shields.io/github/license/messi10tom/InsightExtractor)](https://github.com/messi10tom/InsightExtractor/blob/main/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/messi10tom/InsightExtractor)](https://github.com/messi10tom/InsightExtractor/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/messi10tom/InsightExtractor)](https://github.com/messi10tom/InsightExtractor/commits/main)
![InsightExtractor Banner](./doc/banner.png)

InsightExtractor is an AI-powered tool for automated data retrieval. Connect CSVs or Google Sheets, define queries, and extract structured insights via web search and LLMs. Features include customizable prompts, API integration, and an intuitive dashboard for data export.

## Video Tutorial

For a detailed walkthrough on how to use InsightExtractor, check out our [YouTube video tutorial](https://youtu.be/ATr7Y5CtE1E).

## Supported Models

InsightExtractor supports multiple AI models for data extraction and processing. Users can choose from the following models:

- **Gemini**
- **ChatGPT**
- **Ollama**

Each model offers unique capabilities and can be selected based on the specific requirements of your data extraction tasks.
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
    **Windows**
    ```
    python -m venv IE
    IE\Scripts\activate
    ```
    **macOS and Linux**
    ```
    python3 -m venv IE
    source IE/bin/activate
    ```
    

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:
- **Create BD_AUTH Token**:
    - Visit [Bright Data](https://brightdata.com/) and access the dashboard.
    - Choose "Scraping Browser" from the "Add" dropdown menu.
    - Name your scraping browser (e.g., "InsightExtractor") and create it.
    - Go to "Playground" in your Scraping Browser and toggle to "Code Examples".
    - Select "Python, Selenium" and copy the AUTH key from the example script.
    - Paste the AUTH key into the `BD_AUTH` field in your `.env` file.

- **Create Google Application Credentials**:
    - Visit [Google Cloud Console](https://console.cloud.google.com/) and select your Google account.
    - Create and select a new project.
    - Navigate to "API & Services" and enable the Google Sheets API.
    - Create credentials, set the service account role to Editor, and generate a JSON key.
    - Download the JSON key file and move it to the project directory.
    - Copy the file path and paste it into the `GOOGLE_APPLICATION_CREDENTIALS` field in your `.env` file.

- **Create Google API Key**:
    - Visit [Google AI Studio](https://aistudio.google.com/welcome) and sign in with your Google account.
    - Click on the "Get API key".
    - Click on "Create API Key" to generate a new API key.
    - Copy the generated API key and paste it into the `GOOGLE_API_KEY` field in your `.env` file.

 - **Setting Up ChatGPT API Key**:

    1. **Create an Account**:
        - Sign up for a free account on ChatGPT [here](https://chat.openai.com/).

    2. **Generate an API Key**:
        - Log in, go to "API Keys", click "+ Create new secret key", name your key, and copy the API key.

    3. **Set Up Billing**:
        - Go to 'Billing', add payment details, choose user type, enter payment info, and configure payment options.

    4. **Set Usage Limits**:
        - Go to 'Limits', set hard and soft usage caps, and click 'Save'.

    5. **Save API Key in `.env` File**:
        - Add the following line to your `.env` file:
            ```env
            OPENAI_API_KEY=your_api_key_here
            ```

- **Set Up Ollama**:
    - Visit [Ollama GitHub](https://github.com/ollama/ollama) and download the appropriate version for your operating system.
    - After downloading, open your terminal and run the following command:
        ```sh
        ollama run llama3.2
        ```
- **Set up streamlit secrets**
    - create ```.streamlit\secrets.toml``` and paste all the API keys in the following format
    ```env
    BD_AUTH=""
    GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
    GOOGLE_API_KEY=""
    OPENAI_API_KEY=""
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
    Extract the names, emails, and companies of the professionals mentioned in the text {professional}.
    ```

## Contributing

We welcome contributions to InsightExtractor! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Selenium](https://www.selenium.dev/)
