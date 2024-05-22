from datasets import Dataset
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
import os

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
import logging

logging.basicConfig(
    filename='validation.log',  # file name
    level=logging.INFO,  # log level
    format='%(asctime)s - %(levelname)s - %(message)s')  # log format

folder_path = "/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/All-txt"

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

# Create embeddings for the text chunks using OpenAI's embedding model.
embeddings_model = OpenAIEmbeddings()

# Create an FAISS vector store from the documents to enable efficient similarity search.
db = FAISS.from_documents(texts, embeddings_model)

# Create a retriever that can find relevant text chunks based on the embeddings.
retriever = db.as_retriever()











# 定义 LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# 定义提示模板
template = """You are an assistant for a question-answering task.
Use the following retrieved context snippets to answer the question.
If you do not know the answer, simply say you do not know.
Use no more than two sentences to keep the answer concise.
Question: {question}
Context: {context}
Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

# 设置 RAG 流程
rag_chain = (
    {"context": retriever,  "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)






# 问题
questions = ["What imaging technique was used to study the nuclear pore complex (NPC)?",
             "How does stochastic super-resolution microscopy contribute to the study of NPC structure?",
             "What is the average precision achieved in determining the positions of fluorescent labels within the NPC?",
             "How many individual pores were analyzed to determine the average positions of fluorescent labels?",
             "How does the Nup107-160 subcomplex contribute to the overall structure of the NPC?",
             "How does high content imaging of cell shape and proliferation integrate with gene expression and DNA sequence datasets in analyzing human iPSC lines?",
             "What is the role of the Probabilistic Estimation of Expression Residuals (PEER) in extracting factors from studies involving human iPSC lines?",
             "How do intrinsic conditions, like genetic concordance among cell lines from the same donor, affect cellular behavior in human iPSC studies?",
             "In what ways do extrinsic conditions, such as cell responses to varying fibronectin concentrations, influence the behavior of human iPSCs?",
             "What associations have been found between genes with rare deleterious non-synonymous SNVs and outlier cell behavior in human iPSC studies?"]

          




         
# 真实答案
ground_truths = [[""],
             [""],
             [""],
             [""],
             [""],
             [""],
             [""],
             [""],
             [""],
             [""]
            ]
answers = []
contexts = []


# 推导信息
for query in questions:
  answers.append(rag_chain.invoke(query))
  contexts.append([docs.page_content for docs in retriever.get_relevant_documents(query)])

# 转换为字典
data = {
    "question": questions,   # 问题
    "answer": answers, # 答案
    "contexts": contexts, # 上下文
    "ground_truths": ground_truths  # 真实答案
}


# 将字典转换为数据集
dataset = Dataset.from_dict(data)



result = evaluate(
    dataset = dataset,
    metrics=[
        context_precision,
        # context_recall,
        faithfulness,
        answer_relevancy,
    ],
)

df = result.to_pandas()

df.to_csv('output.csv', index=False)




