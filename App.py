from PyPDF2 import PdfReader
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI

from langchain_community.callbacks.manager import get_openai_callback
from modules.process_data import (extract_text_with_page_numbers,process_text_with_splitter)
from utilities.utils import setup_logger

# Setup logger
Logger = setup_logger(logger_file="app")



def main() -> None:
    """Main application function."""
    # Custom styling
    st.markdown(
        """
    <style>
        .main-title {
            font-size: 2.5em !important;
            color: #2E86C1;
            text-align: center;
            padding: 20px;
            margin-bottom: 25px;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .user-message {
            background-color: #f0f8ff;
            border: 1px solid #2E86C1;
        }
        .assistant-message {
            background-color: #f5f5f5;
            border: 1px solid #5D6D7E;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">📄 DocuChat AI  🤖<br><div style="font-size: 0.6em;">Your Intelligent Document Conversationalist</div></div>',
        unsafe_allow_html=True,
    )

    api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
    if not api_key:
        st.warning("🔑 Please enter your OpenAI API key to proceed")
        st.stop()

    llm = OpenAI(api_key=api_key, temperature=0.3)

    # PDF Upload Section
    pdf = st.sidebar.file_uploader("Upload PDF Document", type="pdf")   

    if pdf is not None:
        Logger.info("PDF uploaded successfully.")

        pdf_reader = PdfReader(pdf)
        text, page_numbers = extract_text_with_page_numbers(pdf_reader)
        Logger.debug(f"Extracted text length: {len(text)} characters.")

        knowledgeBase = process_text_with_splitter(text, page_numbers)

        query = st.chat_input("Ask a question about the document...")
        cancel_button = st.button("Cancel")

        if cancel_button:
            Logger.info("User cancelled the operation.")
            st.stop()

        if query:
            Logger.info(f"Received query: {query}")
            docs = knowledgeBase.similarity_search(query)

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
