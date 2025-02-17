from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper



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
    model = ChatOpenAI(model = "gpt-3.5-turbo")
    prompt = f"""
        Please provide the answer to the question. 
        After answering, identify the document where the answer is located 
        and provide the 'Study Description' and 'Experiment Description' from that document. 
        Additionally, please provide the 'Experiment Description' from three other related documents.
        """
    messages=[
    {
      "role": "user",
      "content": prompt
    }
    ]
    
    # Load the PDF file using a loader that can handle PDF formats.
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

    # Initialize a conversational retrieval chain with the model, retriever, and memory.
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )

    # Invoke the QA chain to get a response to the input question, using the chat history.
    response = qa.invoke({"chat_history": memory, "question": question})

    # Record the returned result
    logging.info(f"Query response for '{question}': {response['answer']}")
    
    # Return the response from the QA system.
    return response