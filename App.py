from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI

from langchain_community.callbacks.manager import get_openai_callback
from modules.process_data import (extract_text_with_page_numbers,process_text_with_splitter)
from utilities.utils import setup_logger

# Setup logger
Logger = setup_logger(logger_file="app")

# Load Env 
load_dotenv()


def main() -> None:
    """Main function to run the Streamlit app."""
    st.title("Chat with your PDF 💬")

    pdf = st.file_uploader("Upload your PDF Document", type="pdf")

    if pdf is not None:
        Logger.info("PDF uploaded successfully.")

        pdf_reader = PdfReader(pdf)
        text, page_numbers = extract_text_with_page_numbers(pdf_reader)
        Logger.debug(f"Extracted text length: {len(text)} characters.")

        knowledgeBase = process_text_with_splitter(text, page_numbers)

        query = st.text_input("Ask a question to the PDF")
        cancel_button = st.button("Cancel")

        if cancel_button:
            Logger.info("User cancelled the operation.")
            st.stop()

        if query:
            Logger.info(f"Received query: {query}")
            docs = knowledgeBase.similarity_search(query)
            Logger.debug(f"Found {len(docs)} similar documents.")

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")

            input_data = {"input_documents": docs, "question": query}

            with get_openai_callback() as cost:
                response = chain.invoke(input=input_data)
                Logger.info(f"Query processed. Cost: {cost}")
                st.write(response["output_text"])
                st.write("Sources:")

            unique_pages = set()

            for doc in docs:
                text_content = getattr(doc, "page_content", "")
                source_page = knowledgeBase.page_info.get(
                    text_content.strip(), "Unknown"
                )

                if source_page not in unique_pages:
                    unique_pages.add(source_page)
                    st.write(f"Chunk Page Number : {source_page}")


if __name__ == "__main__":
    Logger.info("Application started.")
    main()
