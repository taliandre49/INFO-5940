import chromadb.api.client
import streamlit as st
from openai import OpenAI
from openai import AzureOpenAI
from os import environ
# import dotenv
# from dotenv import load_dotenv
import base64
from base64 import b64encode
import PyPDF2
import langchain_openai
from langchain_openai import AzureChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import Document
import chromadb.api

chromadb.api.client.SharedSystemClient.clear_system_cache()


"""
*** STATIC VARIABLES ***
These are the clients, LLMS, and apolication titles DO NOT change these following lines of code
These remain the same despite which version of appliation you want to run

DO NOT TOUCH BELLOW
"""
# Set up Azure OpenAI client
client = AzureOpenAI(
    api_key=environ['AZURE_OPENAI_API_KEY'],
    api_version="2023-03-15-preview",
    azure_endpoint=environ['AZURE_OPENAI_ENDPOINT'],
    azure_deployment=environ['AZURE_OPENAI_MODEL_DEPLOYMENT'],
)

# Set up LLM (Azure GPT model)
llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    temperature=0.2,
    api_version="2023-06-01-preview",
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
st.title("📝 File Q&A with OpenAI")


"""
DO NOT TOUCH ABOVE
"""




"""

***** CHUNKING AFTER PROMPT LOGIC *****

The logic bellow corresponds to the other version of the application where chunking occurs AFTER the user writes a message to the AI
     - This version may cause a more lag when waiting for a response due to chunking during message quering
     - However user will not need to initially wait for chunknig to complete before prompting chatbot
To run this version simply uncomment code bellow and comment out the other code corresponding to the logic for chunking before message.
        - This can be found when searching for CHUNKING BEFORE PROMPT
Save file and re run terminal command `streamlit run chat_upload.py`

"""
# Load environment variables
# # load_dotenv() 

# uploaded_file = st.file_uploader(
#     "Upload an article", 
#     type=("txt", "pdf"),
#     accept_multiple_files=True
# )

# question = st.chat_input(
#     "Ask something about the article",
#     disabled=not uploaded_file,
# )

# # Initialize session state for messages and vectorstore
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

# if "vectorstore" not in st.session_state:
#     st.session_state["vectorstore"] = None

# # Display chat messages
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if uploaded_file and st.session_state["vectorstore"] is None:
#     documents = []
    
#     # Process each uploaded file
#     for file in uploaded_file:
#         file_content = ""
        
#         if file.type == "application/pdf":
#             # If file typ pdf, extract text from PDF
#             pdf_reader = PyPDF2.PdfReader(file)
#             for page in pdf_reader.pages:
#                 file_content += page.extract_text()
                
#         elif file.type == "text/plain":
#             # For txt files, just read the content
#             file_content = file.read().decode("utf-8")
        
#         # Create a single Document object for the whole file with metadata
#         document = Document(
#             page_content=file_content,
#             metadata={"source": file.name} 
#         )
#         #Populate new file for each file uploaded to creat 'database' for RAG
#         documents.append(document)

#     # Initialize the RecursiveCharacterTextSplitter
#     chunk_size = 1000  # chunk size
#     chunk_overlap = 100  # chunk overlap

#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap
#     )

#     # Split the documents into chunks
#     chunks = text_splitter.split_documents(documents)

#     # Initialize Chroma vector store and store it in session_state
#     st.session_state["vectorstore"] = Chroma.from_documents(
#         documents=documents, 
#         embedding=AzureOpenAIEmbeddings(model="text-embedding-3-large")
#     )


# # Retrieve the initialized vector store from session_state
# vectorstore = st.session_state["vectorstore"]

# # Set up the retriever
# if vectorstore:
#     retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})


# # If a question is asked, process the question
# if question and vectorstore:
#     st.session_state.messages.append({"role": "user", "content": question})
#     st.chat_message("user").write(question)

#     # Retrieve relevant documents based on the question
#     retrieved_docs = retriever.invoke(question)
    
#     # Format the retrieved documents
#     def format_docs(docs):
#         return "\n\n".join(doc.page_content for doc in docs)

#     formatted_docs = format_docs(retrieved_docs)
    
#     # Define the prompt template for the LLM
#     template = """
#         You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
#         If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        
#         Question: {question} 
        
#         Context: {context} 
        
#         Answer:
#     """
#     prompt = PromptTemplate.from_template(template)

#     # Set up the retrieval-augmented generation (RAG) chain
#     rag_chain = (
#         {"context": retriever | format_docs, "question": RunnablePassthrough()}
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     # Invoke the chain to get the answer
#     ress = rag_chain.invoke(question)

#     # Display the assistant's response
#     with st.chat_message("assistant"):
#         st.write(ress)

#     # Append the assistant's response to the messages
#     st.session_state.messages.append({"role": "assistant", "content": ress})
# # 


"""""
 ***** CHUNKING BEFROE PROMPT LOGIC ****

    The following code bellow runs the default algorithm logic:
        - This code chunks, splits, and transforms files before the User message
        - This may cause lag before you are able to write a message but will reduce lag when waiting for a response
    To run this code make sure you have the code logic for Chunking after message is commented out and the following lines of logic bellow are uncommented
        - This can be found when searching for CHUNKING AFTER PROMPT
    Save file and re run terminal command `streamlit run chat_upload.py`
"""""
# File uploader
uploaded_file = st.file_uploader(
    "Upload an article", 
    type=("txt", "pdf"),
    accept_multiple_files=True
)

# Initialize session state for messages and vectorstore
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = None

# Chunking process right after file upload
if uploaded_file and st.session_state["vectorstore"] is None:
    documents = []
    
    # Process each uploaded file
    for file in uploaded_file:
        file_content = ""
        
        if file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                file_content += page.extract_text()
                
        elif file.type == "text/plain":
            file_content = file.read().decode("utf-8")
        
        # Create a Document object for each file
        document = Document(
            page_content=file_content,
            metadata={"source": file.name}
        )
        documents.append(document)

    # Chunk the uploaded documents
    chunk_size = 1000
    chunk_overlap = 100
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)

    # Store the chunks in a vector store using Chroma
    st.session_state["vectorstore"] = Chroma.from_documents(
        documents=chunks,  # Use chunks instead of original documents
        embedding=AzureOpenAIEmbeddings(model="text-embedding-3-large")
    )

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User can now ask questions
question = st.chat_input(
    "Ask something about the article",
    disabled=not uploaded_file,
)

# Retrieve the initialized vector store
vectorstore = st.session_state["vectorstore"]

if vectorstore and question:
    # Append user question to session state
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # Set up the retriever and retrieve relevant documents
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    retrieved_docs = retriever.invoke(question)
    
    # Function to format retrieved documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    formatted_docs = format_docs(retrieved_docs)
    
    # Define the prompt template for the LLM
    template = """
        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        
        Question: {question} 
        
        Context: {context} 
        
        Answer:
    """
    prompt = PromptTemplate.from_template(template)

    # RAG chain setup
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Get answer from the RAG chain
    response = rag_chain.invoke(question)

    # Display the assistant's response and append to messages
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})