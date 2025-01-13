import unittest
from unittest.mock import MagicMock
from PyPDF2 import PdfReader
from utilities.utils import setup_logger
from langchain_community.vectorstores import FAISS

from modules.process_data import (extract_text_with_page_numbers, process_text_with_splitter) 


class TestPDFProcessing(unittest.TestCase):
    def setUp(self):
        self.logger = setup_logger(logger_file="app")
        
        # Mocking PdfReader and its methods for testing
        self.mock_pdf = MagicMock(spec=PdfReader)
        self.mock_pdf.pages = [MagicMock(), MagicMock()]
        self.mock_pdf.pages[0].extract_text.return_value = "Page 1 text."
        self.mock_pdf.pages[1].extract_text.return_value = "Page 2 text."

    def test_extract_text_with_page_numbers(self):
        text, page_numbers = extract_text_with_page_numbers(self.mock_pdf)
        
        expected_text = "Page 1 text.Page 2 text."
        expected_page_numbers = [1] * 1 + [2] * 1
        
        self.assertEqual(text, expected_text)
        self.assertEqual(page_numbers, expected_page_numbers)

    def test_extract_text_with_empty_page(self):
        self.mock_pdf.pages[1].extract_text.return_value = None
        
        text, page_numbers = extract_text_with_page_numbers(self.mock_pdf)
        
        expected_text = "Page 1 text."
        expected_page_numbers = [1] * 1
        
        self.assertEqual(text, expected_text)
        self.assertEqual(page_numbers, expected_page_numbers)

    def test_process_text_with_splitter(self):
        text = "Sample text for testing."
        page_numbers = [1] * 3
        
        knowledge_base = process_text_with_splitter(text, page_numbers)
        
        self.assertIsInstance(knowledge_base, FAISS)
        self.assertEqual(len(knowledge_base.page_info), 1)  
        
if __name__ == '__main__':
    unittest.main()
