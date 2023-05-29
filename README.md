# chatWithPDF
This project allows you to upload a PDF document and ask questions about its content. It uses langchain, openapi ai model and  Facebook Ai Similarity Search(FAISS) library to process the text in the PDF and provide answers to questions pertaining the document.

# Project Screen
[]()

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/john-thuo1/chatWithPDF
   cd into your directory/ open with vscode
   ```
2. Create a Virtual Environment:
    ```shell
    python -m venv env
    ```
3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```
4. Create OpenAI API Key and add it to your .env file:
   [openai](https://platform.openai.com/)
   
5. Run the application:

   ```shell
   streamlit run App.py
   ```
