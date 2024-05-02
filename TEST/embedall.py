from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import logging
import numpy as np

load_dotenv()  # Load environment variables from a .env file.
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

# Configuring Log Files and Formats
logging.basicConfig(
    filename='embedall.log',  # file name changed to embedall.log
    level=logging.INFO,  # log level
    format='%(asctime)s - %(levelname)s - %(message)s')  # log format

def read_texts_and_paths(root_dir):
    texts, metadata = [], []
    logging.info(f"Starting to read texts from directory: {root_dir}")
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                filepath = os.path.join(dirpath, filename)
                study_id = os.path.basename(os.path.dirname(filepath))
                with open(filepath, 'r', encoding='utf-8') as file:
                    texts.append(file.read())
                    metadata.append(f"{study_id}: {filepath}")
                logging.info(f"Processed file: {filepath}")
    return texts, metadata

def embed_texts(texts):
    logging.info("Starting text embedding process")
    # Initialize the OpenAIEmbeddings with the specified model
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")  # Adjust model as needed

    embeddings = []
    for text in texts:
        # Use the OpenAIEmbeddings to generate embeddings
        doc_result = embeddings_model.embed_documents([text])
        embeddings.append(doc_result[0])  # Assuming doc_result[0] contains the embedding array
    logging.info("Text embedding completed")
    return np.vstack(embeddings)  # Stack embeddings into

def create_faiss_index(embeddings):
    logging.info("Creating FAISS index")
    d = embeddings.shape[1]  # Dimension of the embeddings
    # Create a FAISS index for L2 distance
    index = FAISS.create_index("Flat", d)  # Assuming 'Flat' creates an IndexFlatL2 equivalent
    index.add(embeddings.astype(np.float32))  # Add embeddings to the index
    logging.info("FAISS index created")
    return index

def save_index_and_metadata(index, metadata, index_path, metadata_path):
    logging.info("Saving FAISS index and metadata")
    FAISS.write_index(index, index_path)
    with open(metadata_path, 'w') as f:
        for data in metadata:
            f.write(f"{data}\n")
    logging.info("FAISS index and metadata saved")

# Main execution
root_dir = 'TEST/IDR'
index_path = 'your_index.faiss'
metadata_path = 'your_metadata.txt'

logging.info("Script started")
texts, metadata = read_texts_and_paths(root_dir)
embeddings = embed_texts(texts)
index = create_faiss_index(texts, embeddings)
save_index_and_metadata(index, metadata, index_path, metadata_path)
logging.info("Script completed")