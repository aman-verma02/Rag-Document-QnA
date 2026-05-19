# Defining custom exceptions for the application to handle specific error scenarios gracefully.



class PDFProcessingError(Exception):
    """Exception raised for errors in the PDF processing."""
    pass


class EmbeddingError(Exception):
    """Exception raised for errors in the embedding generation."""
    pass


class VectorStoreError(Exception):
    """Exception raised for errors in the vector store."""
    pass


class LLMError(Exception):
    """Exception raised for errors in the LLM."""
    pass

class PipelineError(Exception):
    """Exception raised for errors in the RAG pipeline."""
    pass