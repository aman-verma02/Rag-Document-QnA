# These embeddings are created for the data as machine can only understand numbers


from sentence_transformers import SentenceTransformer
from logging import getLogger
from .exceptions import EmbeddingError
logger = getLogger(__name__)


class EmbeddingGenerator: 
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the EmbeddingGenerator with the specified embedding model.
        Args:
            model_name (str): The name of the embedding model to use. Default is 'all-MiniLM-L6-v2'.
        """
        try: 
            self.model = SentenceTransformer(model_name)
            logger.info(f"Embedding model initialized: {model_name}")
        except Exception as e:
            logger.error(f"Error in initializing embedding model: {e}")
            raise EmbeddingError(f"Error in initializing embedding model: {e}")

    def generate(self, text: str):
        """
        Generates embeddings for the given text.
        Args:
            text (str): The text for which to generate embeddings.
        Returns:
            torch.Tensor: The generated embeddings.
        """
        try:
            embedding = self.model.encode(text, convert_to_tensor=True)
            logger.info("Embedding generated successfully.")
            return embedding
        except Exception as e:
            logger.error(f"Error in generating embedding: {e}")
            raise EmbeddingError(f"Error in generating embedding: {e}")


     # Why batch processing ?   : When you call encode() on a list of texts all at once, the model processes them in parallel using matrix operations. This is how GPUs and even optimized CPUs work — they're built for parallel math.
    def generate_batch(self, texts: list):
        """
        Generates embeddings for a batch of texts.
    
        Args:           
            texts (list): A list of texts for which to generate embeddings.
        Returns:            
            torch.Tensor: The generated embeddings for the batch of texts.
        """
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=True)
            logger.info("Batch embeddings generated successfully.")
            return embeddings
        except Exception as e:
            logger.error(f"Error in generating batch embeddings: {e}")
            raise EmbeddingError(f"Error in generating batch embeddings: {e}")