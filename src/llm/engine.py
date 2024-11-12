import re
import ast
from langchain_ollama import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document
# from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_chroma import Chroma
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Create a template string
template = """
You are an intelligent assistant helping to process web-scraped data in response to a user’s query.

**Input Data:**
- **WEB_DATA**: {WEB_DATA}
- **CSV_DATA**: {CSV_DATA}
- **USER_PROMPT**: {USER_PROMPT}

**Task**:
- Only extract the information the user specifically requested in the **USER_PROMPT**.
- Ensure the response data includes only information present in **WEB_DATA** and **CSV_DATA**.
- Format the output in JSON for easy processing.
- Exclude any data not explicitly mentioned in the **CSV_DATA** or **WEB_DATA**.

**Output Example**:
```json
{{
  "result": [
    {{ "name": "Alex Thompson", "company": "Innovatech Corp", "email": "alex.thompson@example.com" }},
    {{ "name": "Jamie Reed", "company": "Synergy Solutions", "email": "jamie.reed@example.com" }},
    {{ "name": "Taylor Morgan", "company": "Quantum Dynamics", "email": "taylor.morgan@example.com" }},
    {{ "name": "Jordan Lee", "company": "Vertex Ventures", "email": "jordan.lee@example.com" }},
    {{ "name": "Casey Walker", "company": "Stellar Innovations", "email": "casey.walker@example.com" }}
  ]
}}
"""


id = "llama3.2:1b"

# TODO: implement placeholder for users to add

def get_entity_from_ollama(web_data: str, 
                           csv_data: str, 
                           user_prompt: str) -> str:


    embeddings = OllamaEmbeddings(model=id)
    model = OllamaLLM(model=id)
    context = [Document(page_content=web_data)]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(context)
    vectorstore = InMemoryVectorStore(embeddings)
    vectorstore.add_documents(documents=splits)
    # vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

    # Retrieve and generate using the relevant snippets of the web data.
    retriever = vectorstore.as_retriever()
    retrieved_docs = retriever.get_relevant_documents(user_prompt)
 
    # Combine retrieved documents into a single string
    retrieved_docs = "\n".join([doc.page_content for doc in retrieved_docs])

    # Create a template 
    prompt = ChatPromptTemplate.from_template(template)
    print("prompt created")
    print(prompt)
    
    rag_chain = (
    {
            "WEB_DATA": lambda x: x,  
            "CSV_DATA": lambda x: x,  # Join data entities as a string
            "USER_PROMPT": lambda x: x  # Pass the user prompt as a string
    }
    | prompt
    | model
    | format_output)
    
    return rag_chain.invoke({"WEB_DATA": retrieved_docs, 
                             "CSV_DATA": csv_data, 
                             "USER_PROMPT": user_prompt})

def format_output(output: str) -> list:
    # Extract the JSON-like list from the output string
    match = re.search(r'\[.*\]', output, re.DOTALL)
    if match:
        extracted_data = match.group(0)
        # Convert the string to a list of dictionaries
        return ast.literal_eval(extracted_data)
    return 

def preprocess_df_for_llm(df):
  """Preprocesses a Pandas DataFrame for LLM input.

  Args:
    df: The Pandas DataFrame to preprocess.

  Returns:
    A string representation of the DataFrame suitable for LLM input.
  """

  # Convert DataFrame to string without index
  df_string = df.to_string(index=False)

  return df_string

