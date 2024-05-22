import streamlit as st
import os

from langchain.memory import ConversationBufferMemory
from UtilsWithSource import qa_agent
from FormetDoc import format_retrieved_documents
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file.
# Invoke OpenAI API key.
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment.")

# Set up the title of the Streamlit application.
st.title("📑 IDR Smart Search Engine")

# Initialize session state for conversation memory if it does not exist.
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,  # Enable returning of messages in the conversation
        memory_key="chat_history",  # Key used to store chat history in memory
        output_key="answer"  # Key used to store answers in the memory
    )

temp_file_path = "/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/All-txt"

# Create a text input widget to take a search query, disabled if no file is uploaded.
"🚀 Welcome to intelligent search engine powered by IDR (Image Data Resource) . "
"💬 Here, you can search for the data and information you need through conversation. "

"🐣 For example, you might say: I want to find some images related to embryology," 
"   or Show me the latest images from Professor Harry Fischl's articles 📚." 

"🌟 This platform is designed to make your searches easier and more intuitive, catering to your specific needs."

question = st.text_input("Now, start to ask questions here", disabled=not temp_file_path)







# Display a warning if the OpenAI API key is not entered.
if temp_file_path and question and not openai_api_key:
    st.info("Please enter OpenAI API key")

# Process the file and the question if both are provided and the API key is available.
if temp_file_path and question and openai_api_key:
    with st.spinner("Hold tight, answer is on the way ⏳"):  # Display a spinning loading indicator during processing.
        # Call the qa_agent function to process the uploaded document and question.
        
        response = qa_agent(st.session_state["memory"], temp_file_path, question)
    st.write("### Answer")  # Output the section heading 'answer'.
    st.write(response["answer"])  # Display the retrieved answer.
    # st.write(response["context"])  # Display the context of retrieved answer.

    st.write("### Source of the answer")  # Output the section heading 'answer'.
    raw_context = response["context"]
    format_context = format_retrieved_documents(raw_context)
    st.write(format_context) 
    

    # Update chat history in session state with the new interaction.
    st.session_state["chat_history"] = response["chat_history"]

# Display the chat_history.
if "chat_history" in st.session_state:
    with st.expander("history message"):  # Use an expander for history messages, create a panel that can be expanded and collapsed.
        # Iterate over the chat history and display each message.
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.write(human_message.content)  # Display the human message content.
            st.write(ai_message.content)  # Display the AI response content.
            # Add a divider between conversations for clarity.
            if i < len(st.session_state["chat_history"]) - 2:
                st.divider()
