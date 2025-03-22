from typing import Tuple, Set
from PyPDF2 import PdfReader
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.memory import ConversationBufferMemory
from modules.process_data import (
    extract_text_with_page_numbers,
    process_text_with_splitter,
)
from utilities.utils import setup_logger

# Initialize logger
logger = setup_logger(logger_file="app")


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "knowledge_base" not in st.session_state:
        st.session_state.knowledge_base = None
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )


def display_chat_messages():
    """Display chat messages in a styled format."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("View Sources"):
                    for source in message["sources"]:
                        st.write(f"📄 Page {source}")


def process_query(query: str, llm: OpenAI) -> Tuple[str, Set[int]]:
    """Process user query with contextual memory."""
    with st.spinner("Analyzing document..."):
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=st.session_state.knowledge_base.as_retriever(),
            memory=st.session_state.memory,
        )

        with get_openai_callback() as cost:
            response = qa_chain({"question": query})
            logger.info(f"Query processed. Cost: {cost}")

            sources = set()
            for doc in response.get("source_documents", []):
                text_content = getattr(doc, "page_content", "").strip()
                source_page = st.session_state.knowledge_base.page_info.get(
                    text_content, "Unknown"
                )
                sources.add(source_page)

            return response["answer"], sources


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

    initialize_session_state()

    api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
    if not api_key:
        st.warning("🔑 Please enter your OpenAI API key to proceed")
        st.stop()

    llm = OpenAI(api_key=api_key, temperature=0.3)

    # PDF Upload Section
    pdf = st.sidebar.file_uploader("Upload PDF Document", type="pdf")
    if pdf:
        if "processed" not in st.session_state or st.session_state.pdf_hash != hash(
            pdf.getvalue()
        ):
            with st.spinner("Processing PDF..."):
                pdf_reader = PdfReader(pdf)
                text, page_numbers = extract_text_with_page_numbers(pdf_reader)
                st.session_state.knowledge_base = process_text_with_splitter(
                    text, page_numbers
                )
                st.session_state.pdf_hash = hash(pdf.getvalue())
                st.session_state.chat_history = []
                st.session_state.memory.clear()
            st.success("✅ Document processed successfully!")

    display_chat_messages()

    # Chat input
    query = st.chat_input("Ask a question about the document...")
    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})

        response, sources = process_query(query, llm)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": response, "sources": sources}
        )

        st.rerun()


if __name__ == "__main__":
    logger.info("Application started")
    main()
