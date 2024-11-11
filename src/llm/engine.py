from langchain_ollama import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Create a template string
template = """You are provided with the following web-scraped text data:

{WEB_DATA}

The user is interested in extracting specific data entities from the above text. The data entities to be extracted are:

{DATA_ENTITY}

The user has provided the following prompt to explain what they want in more detail:

{USER_PROMPT}

Based on the user's prompt and the provided web-scraped text data, extract the relevant data entities and present them in the following JSON format:

[
    {{"name": "data entity 1", "value": "extracted value 1"}},
    {{"name": "data entity 2", "value": "extracted value 2"}},
    ...
]

Please ensure that the extracted values are accurate and relevant to the user's prompt.
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
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

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
    | StrOutputParser())
    
    return rag_chain.invoke({"WEB_DATA": retrieved_docs, 
                             "DATA_ENTITY": data_entity, 
                             "USER_PROMPT": user_prompt})

    
def formated_output(output: str) -> str:
    
    return output


