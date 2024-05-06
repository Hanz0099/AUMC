from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv
import logging
import os


load_dotenv()  # Load environment variables from a .env file.
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

# Configuring Log Files and Formats
logging.basicConfig(
    filename='database_access_bot.log',  # file name
    level=logging.INFO,  # log level
    format='%(asctime)s - %(levelname)s - %(message)s')  # log format

# Load the document using TextLoader
loader = TextLoader("/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/实践/AUMC/TEST/IDR/idr001-heriche-condensation/idr0002-study.txt")
documents = loader.load()
print(f"Number of documents loaded: {len(documents)}")

# Split the loaded document into chunks using CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=5, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
print(f"Number of chunks created: {len(docs)}")

# Generate embeddings using OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

# Create a FAISS index from the document chunks and their embeddings
db = FAISS.from_documents(docs, embeddings)

# Print the total number of items in the FAISS index
print(f"Number of items in the FAISS index: {db.index.ntotal}")

# Query the FAISS index with a specific question
query = "show me the link of example images"
docs = db.similarity_search(query)

# Display the most relevant result
print(docs[0].page_content)


