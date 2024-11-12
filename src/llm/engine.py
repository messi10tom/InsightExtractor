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
You are provided with the following web-scraped text data:

{WEB_DATA}

Extract the following data entities from the text:

{DATA_ENTITY}

User's prompt for more details:

{USER_PROMPT}

**Example for illustration only (do not include this in the output):**
WEB_DATA: Alex Thompson is a dedicated professional at Innovatech Corp, reachable via alex.thompson@example.com.
Jamie Reed, a key contributor at Synergy Solutions, can be contacted at jamie.reed@example.com.
Taylor Morgan brings innovation to Quantum Dynamics, and is accessible through taylor.morgan@example.com.
Jordan Lee is an integral part of Vertex Ventures and can be reached at jordan.lee@example.com.
Casey Walker works at Stellar Innovations, with an email contact of casey.walker@example.com.
DATA_ENTITY: name, email, company
USER_PROMPT: Extract the names, emails, and companies of the professionals mentioned in the website.
**Expected output (do not copy this directly):**
[
    {{"name": "Alex Thompson", "email": "alex.thompson@example.com", "company": "Innovatech Corp"}},
    {{"name": "Jamie Reed", "email": "jamie.reed@example.com", "company": "Synergy Solutions"}},
    {{"name": "Taylor Morgan", "email": "taylor.morgan@example.com", "company": "Quantum Dynamics"}},
    {{"name": "Jordan Lee", "email": "jordan.lee@example.com", "company": "Vertex Ventures"}},
    {{"name": "Casey Walker", "email": "casey.walker@example.com", "company": "Stellar Innovations"}}
]

**Note:** The example is only to guide the format. Do not include any part of the example in your response. Generate the output based only on the {WEB_DATA} provided.

"""


id = "llama3.2:1b"

# TODO: implement placeholder for users to add

def get_entity_from_ollama(web_data: str, 
                           data_entity: list, 
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

    # Format the data_entity list into a string
    data_entity = "\n".join(data_entity)
    # Create a template 
    prompt = ChatPromptTemplate.from_template(template)
    print("prompt created")
    print(prompt)
    
    rag_chain = (
    {
            "WEB_DATA": lambda x: x,  
            "DATA_ENTITY": lambda x: x,  # Join data entities as a string
            "USER_PROMPT": lambda x: x  # Pass the user prompt as a string
    }
    | prompt
    | model
    | format_output)
    
    return rag_chain.invoke({"WEB_DATA": retrieved_docs, 
                             "DATA_ENTITY": data_entity, 
                             "USER_PROMPT": user_prompt})

def format_output(output: str) -> list:
    # Extract the JSON-like list from the output string
    match = re.search(r'\[.*\]', output, re.DOTALL)
    if match:
        extracted_data = match.group(0)
        # Convert the string to a list of dictionaries
        return ast.literal_eval(extracted_data)
    return 

