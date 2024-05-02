import streamlit as st
import os

from langchain.memory import ConversationBufferMemory
from Utils import qa_agent
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

# Create a file uploader widget to upload PDF documents.
uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")

# Create a text input widget to take a search query, disabled if no file is uploaded.
question = st.text_input("What data you want to search", disabled=not uploaded_file)



# Display a warning if the OpenAI API key is not entered.
if uploaded_file and question and not openai_api_key:
    st.info("Please enter OpenAI API key")

# Process the file and the question if both are provided and the API key is available.
if uploaded_file and question and openai_api_key:
    with st.spinner("Searching, hold me please"):  # Display a spinning loading indicator during processing.
        # Call the qa_agent function to process the uploaded document and question.
        response = qa_agent(st.session_state["memory"], uploaded_file, question)
    st.write("### answer")  # Output the section heading 'answer'.
    st.write(response["answer"])  # Display the retrieved answer.
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
