import streamlit as st
from typing import  Dict, Any, Optional, List
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_community.callbacks.manager import get_openai_callback
from modules.process_data import extract_text_with_page_numbers, process_text_with_splitter  
from utilities.utils import setup_logger

# Setup logger
Logger = setup_logger(logger_file="app")

def load_css(file_path: str) -> None:
    """Load custom CSS from file."""
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



def main() -> None:
    """Main application function."""
    # Load external CSS
    load_css("utilities/styles/main.css")

    st.markdown(
        '<div class="main-title">📄 DocuChat AI  🤖<br>'
        '<div style="font-size: 0.6em;">Your Intelligent PDF Document Conversationalist</div></div>',
        unsafe_allow_html=True,
    )

    api_key: str = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
    if not api_key:
        st.warning("🔑 Please enter your OpenAI API key to proceed")
        st.stop()

    llm: OpenAI = OpenAI(api_key=api_key, temperature=0.3)

    # PDF Upload Section
    pdf: Optional[st.runtime.uploaded_file_manager.UploadedFile] = st.sidebar.file_uploader("Upload PDF Document", type="pdf")   

    if pdf is not None:
        Logger.info("PDF uploaded successfully.")

        full_text, page_texts = extract_text_with_page_numbers(pdf)
        Logger.debug(f"Extracted text length: {len(full_text)} characters.")

        knowledgeBase: Any = process_text_with_splitter(full_text, page_texts)

        query: str = st.chat_input("Ask a question about the document...")
        cancel_button: bool = st.button("Cancel")

        if cancel_button:
            Logger.info("User cancelled the operation.")
            st.stop()

        if query:
            Logger.info(f"Received query: {query}")
            docs: List[Any] = knowledgeBase.similarity_search(query)

            chain: Any = load_qa_chain(llm, chain_type="stuff")

            input_data: Dict[str, Any] = {"input_documents": docs, "question": query}

            with get_openai_callback() as cost:
                response: Dict[str, Any] = chain.invoke(input=input_data)
                Logger.info(f"Query processed. Cost: {cost}")
                st.write(response["output_text"])
                st.write("Sources:")

            unique_pages: set = set()
            for doc in docs:
                text_content: str = getattr(doc, "page_content", "")
                source_page: Any = knowledgeBase.page_info.get(text_content.strip(), "Unknown")
                if source_page not in unique_pages:
                    unique_pages.add(source_page)
                    st.write(f"Chunk Page Number : {source_page}")

if __name__ == "__main__":
    Logger.info("Application started.")
    main()