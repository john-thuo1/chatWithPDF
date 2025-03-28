from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from utilities.utils import setup_logger
from typing import IO, Dict, Tuple, List
import pymupdf



Logger = setup_logger(logger_file="app")


def extract_text_with_page_numbers(pdf_file: IO[bytes]) -> Tuple[str, Dict[int, str]]:
    """
    Use PyMuPDF (imported as pymupdf) to extract text from the PDF while keeping track of page numbers.

    Args:
        pdf_file (IO[bytes]): A binary file-like object containing the PDF.

    Returns:
        Tuple[str, Dict[int, str]]:
            - full_text: Concatenated text from all pages.
            - page_texts: Dictionary mapping page numbers (1-indexed) to their respective text.
    """
    pdf_file.seek(0)
    # Open the PDF using the new pymupdf API
    doc = pymupdf.open(stream=pdf_file.read(), filetype="pdf")
    full_text: str = ""
    page_texts: Dict[int, str] = {}
    for i, page in enumerate(doc):
        text: str = page.get_text("text")
        full_text += text + "\n"
        page_texts[i + 1] = text
    return full_text, page_texts


def process_text_with_splitter(text: str, page_numbers: List[int]) -> FAISS:

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    # Split the text
    chunks = text_splitter.split_text(text)
    Logger.debug(f"Text split into {len(chunks)} chunks.")

    embeddings = OpenAIEmbeddings()
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    Logger.info("Knowledge base created from text chunks.")

    # Store the chunks with their corresponding page numbers
    knowledgeBase.page_info = {chunk: page_numbers[i] for i, chunk in enumerate(chunks)}

    return knowledgeBase
