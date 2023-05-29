# chatWithPDF
This project allows you to upload a PDF document and ask questions about its content. It uses langchain, openapi ai model and  Facebook Ai Similarity Search(FAISS) library to process the text in the PDF and provide answers to questions pertaining the document.

## Project Screen
![image](https://github.com/john-thuo1/chatWithPDF/assets/108690517/d4565154-de20-4fe2-9213-f8bb2c66138b)
### Cost
![image](https://github.com/john-thuo1/chatWithPDF/assets/108690517/c4a72a25-1aeb-447c-b4f4-90b38225f9d3)

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

## Next Steps
1. Add support for multiple file formats
2. Implement Document Indexing techniques by use of libraries such as  Elasticsearch or Apache Solr 
3. Enhance question answering capabilities: Explore advanced question answering techniques, such as using transformer models like BERT or    GPT, to improve the accuracy and comprehension of the system.
4. Use a model that supports multiple languages, most notably some BERT models do support this.
