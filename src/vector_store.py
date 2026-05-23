# Its a database where we will store the vectorized data and will use it for the retrieval of relevant data when a query is made.



import faiss
from logging import getLogger
import numpy as np 
from exception.exception import RagSystemException
import sys
from logging.logger import logging

logger = getLogger(__name__)



class VectorStore:
    def __init__(self, dimensions):
        """
        Initializes the VectorStore with the specified dimensions for the embeddings.
        Args:
            dimensions (int): The number of dimensions for the embeddings (e.g., 384 for 'all-MiniLM-L6-v2').
        """
        try: 
            self.faiss_index = faiss.IndexFlatL2(dimensions)  # Assuming 384-dimensional embeddings
            self.chunk_storage = []  # A list to store the corresponding text chunks
            logging.info("Vector store initialized successfully.")
        except Exception as e:
            raise RagSystemException(f"Error in initializing vector store: {e}", sys)
        
    def _to_numpy(self, tensor):
        try: 
            if hasattr(tensor, 'cpu'):
                return tensor.cpu().numpy()
            return np.array(tensor)
        except Exception as e:
            logging.error(f"Error in converting tensor to numpy array: {e}")
            raise RagSystemException(f"Error in converting tensor to numpy array: {e}", sys)
        
    
    def add_chunks(self, chunks, embeddings):
        """
        Adds chunks and their corresponding embeddings to the vector store.
        Args:
            chunks (list): A list of text chunks to be added to the store.
            embeddings (torch.Tensor): A tensor containing the corresponding embeddings for the chunks.
        """
        try: 
            self.chunk_storage.extend(chunks) # Add chunks to the chunk storage
            self.faiss_index.add(self._to_numpy(embeddings)) # Add embeddings to the FAISS index
            logging.info("Chunks added to vector store successfully.")
        except Exception as e:
            raise RagSystemException(f"Error in adding chunks to vector store: {e}", sys)




    def search(self, query_vector, k = 5):
        """
        Searches for the most relevant chunks based on the query embedding.
        Args:
            query_vector (torch.Tensor): The embedding of the query.
            k (int): The number of top relevant chunks to return.
        Returns:
            list: A list of the top_k most relevant text chunks.
        """
        try:
            query_vector = self._to_numpy(query_vector).reshape(1, -1)  # reshape(1, -1) means "1 row, figure out the columns automatically".
            # Reshape the query vector for FAISS as it expects a 2D array so we reshape it to have one row and as many columns as the dimensions of the embedding.
            distances, indices = self.faiss_index.search(query_vector, k)
            # k = number of results you want
            logging.info(f"Search results - Distances: {distances}, Indices: {indices}")
            return [self.chunk_storage[i] for i in indices[0]]
        except Exception as e:
            raise RagSystemException(f"Error in searching vector store: {e}", sys)



    def get_chunks(self, indices): 
        """
        Retrieves the text chunks corresponding to the given indices.
        Args:
            indices (list): A list of indices for which to retrieve the corresponding text chunks.
        Returns:
            list: A list of text chunks corresponding to the given indices.
        """
        try: 
            return [self.chunk_storage[i] for i in indices]
        except Exception as e:
            raise RagSystemException(f"Error in retrieving chunks from vector store: {e}", sys)