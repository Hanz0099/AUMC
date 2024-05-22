from langchain.chains import (
    StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
)
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.output_parsers import StrOutputParser
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel

from dotenv import load_dotenv
import os



import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import logging


load_dotenv()  # Load environment variables from a .env file.
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")


# Configuring Log Files and Formats
logging.basicConfig(
    filename='database_access_bot.log',  # file name
    level=logging.INFO,  # log level
    format='%(asctime)s - %(levelname)s - %(message)s')  # log format

def qa_agent(memory, folder_path, question):
    # Initialize the model using OpenAI's API, specifying the model version.
    
    
    # Load the  file using a loader that can handle txt formats.
    loaders = [TextLoader(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if f.endswith(".txt")]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    # Split the document text into manageable chunks for processing.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # The maximum size of text chunks.
        chunk_overlap=50,  # The overlap between chunks to ensure continuity.
        separators=["\n", ".", "!", "?", ";", ",", ":"]  # Characters that define the boundaries of chunks.
    )
    texts = text_splitter.split_documents(docs)

    # Embedding step is to generate a numerical representation of the data
    # FAISS step is to optimize the storage and querying efficiency of these numerical data.


    # Create embeddings for the text chunks using OpenAI's embedding model.
    embeddings_model = OpenAIEmbeddings()
    
    # Create an FAISS vector store from the documents to enable efficient similarity search.
    db = FAISS.from_documents(texts, embeddings_model)
    
    # Create a retriever that can find relevant text chunks based on the embeddings.
    retriever = db.as_retriever()
  

    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    def format_docs(texts):
        return "\n\n".join(doc.page_content for doc in texts)

    
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    response = rag_chain_with_source.invoke(question)

    return response  








""" 
    formatted_retriever = LambdaRunnable(lambda x: format_docs(x["context"]), retriever)

    rag_chain = RunnableSequence(
      formatted_retriever,
      prompt,
      llm,
      StrOutputParser()
    )
    response = rag_chain.invoke(question)
    
    return response
    """

    