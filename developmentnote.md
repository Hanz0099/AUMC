streamlit run Main.py
pip install --upgrade langchain langchain-community langchainhub langchain-openai langchain-chroma bs4

MainWithSource - Building an interactive interface to invoke functions
UtilsWithSource - Main function, invoking OpenAI to retrieve document information
FormetDoc - Ensure that the output source information is formatted neatly and consistently.
GetAllTxt - Retrieve text documents from all metadata databases.
GetRQ - Get research questions from txt document
RelevancyScore - Validation part, get the relevancy score between text and abstract