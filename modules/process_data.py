from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from utilities.utils import setup_logger
from typing import List, Tuple


Logger = setup_logger(logger_file="app")


def extract_text_with_page_numbers(pdf) -> Tuple[str, List[int]]:
    text = ""
    page_numbers = []

    for page_number, page in enumerate(pdf.pages, start=1):
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text
            page_numbers.extend([page_number] * len(extracted_text.split("\n")))
        else:
            Logger.warning(f"No text found on page {page_number}.")

    return text, page_numbers


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
