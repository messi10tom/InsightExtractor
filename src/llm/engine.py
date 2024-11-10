from langchain_ollama import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.docstore.document import Document
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
    {"name": "data entity 1", "value": "extracted value 1"},
    {"name": "data entity 2", "value": "extracted value 2"},
    ...
]

Please ensure that the extracted values are accurate and relevant to the user's prompt.
"""


id = "llama3.2:1b"

# TODO: implement placeholder for users to add

def get_entity_from_ollama(web_data: list, 
                           data_entity: list, 
                           user_prompt: str) -> str:
    
    embeddings = OllamaEmbeddings(model=id)
    model = OllamaLLM(model=id)
    context = [Document(page_content=doc) for doc in web_data]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(context)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    # Retrieve and generate using the relevant snippets of the web data.
    retriever = vectorstore.as_retriever()

    # Create a template 
    prompt = ChatPromptTemplate.from_template(template)
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
    {"WEB_DATA": retriever | format_docs,  "DATA_ENTITY": data_entity, "USER_PROMPT": user_prompt}
    | prompt
    | model
    | StrOutputParser()
)
    return rag_chain.invoke()


    
get_entity_from_ollama(["This is a sample text data from the web"], ["data entity 1", "data entity 2"], "User's prompt")
