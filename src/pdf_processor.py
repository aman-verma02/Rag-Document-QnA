# This will process the PDF file when a PDF file is uploaded and will pass the processed data to the next stage


import fitz 
import re
import logging
import sys
from exception.exception import RagSystemException
from logging.logger import logging

class PDFProcessor : 

    def __init__(self, chunk_size, chunk_overlap):
        """
        Initializes the PDFProcessor with the specified chunk size and chunk overlap.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap


    def extract_text(self, file_path):
        """
        Extracts text from a PDF file.
        """
        try :
            # code to extract text from PDF file
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            logging.info("Text extracted successfully from PDF file.")
            return text
        
        except Exception as e:
            logging.error(f"Error in extracting text from PDF file: {e}")
            raise RagSystemException(f"Error in extracting text from PDF file: {e}", sys)

    
    def clean_text(self, text): 
        """
        Cleans the extracted text and removes any unwanted characters or formatting.
        """
        try: 
            # code to clean the extracted text
            cleaned_text = text.replace("\n", " ").replace("\r", " ").strip()
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            logging.info("Text cleaned successfully.")
            return cleaned_text
        
        except Exception as e:
            logging.error(f"Error in cleaning text: {e}")
            raise RagSystemException(f"Error in cleaning text: {e}", sys)

    
    def chunk_text(self, text):
        """
        Chunks the cleaned text into smaller pieces.
        """

        try: 
            words= text.split()     # convert text string into list of words

            # code to chunk the cleaned text
            chunks = []
            for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
                chunk = " ".join(words[i:i + self.chunk_size])
                chunks.append(chunk)
            logging.info(f"Text chunked successfully into {len(chunks)} chunks.")
            return chunks
        
        except Exception as e:
            logging.error(f"Error in chunking text: {e}")
            raise RagSystemException(f"Error in chunking text: {e}", sys)


    def process(self, file_path): 
        """
        Processes a PDF file and returns the processed chunks.
        Takes file_path as input
        Calls  extract_text → clean_text → chunk_text internally
        Returns the final list of chunks
        """

        text = self.extract_text(file_path)
        cleaned_text = self.clean_text(text)
        chunks = self.chunk_text(cleaned_text)
        logging.info("PDF processing completed successfully.")
        return chunks     # return the final list of chunks