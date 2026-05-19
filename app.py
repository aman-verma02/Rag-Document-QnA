# app.py - It is the point where uses will interact with the components of the application without actually seeing the internal working of the application. 


import streamlit as st
from src.pipeline import RAGPipeline
from src.exceptions import PipelineError
from logging import getLogger
import tempfile
import os
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = getLogger(__name__)




st.set_page_config(page_title="RAG App", page_icon=":robot:")      # page title and icon
st.title("🤖 Retrieval-Augmented Generation App")
st.markdown("*Upload a research paper and ask questions about it*")


# Store pipeline in session state
if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()

# Store whether PDF is ingested
if "pdf_ingested" not in st.session_state:
    st.session_state.pdf_ingested = False
if "ingested_filename" not in st.session_state:
    st.session_state.ingested_filename = None


logger.info("Streamlit app initialized successfully.")
st.sidebar.header("📄 Document Upload")
st.sidebar.markdown("---")  # divider line


uploaded_file = st.sidebar.file_uploader("Choose PDF", type="pdf")
if uploaded_file is not None:
    # file was uploaded, do something       # upload PDF
    if uploaded_file.name != st.session_state.ingested_filename:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name
            st.session_state.pipeline.ingest(tmp_path)  # Ingest the PDF file using the pipeline
            st.session_state.pdf_ingested = True  # Set the flag to indicate that PDF has been ingested
            st.session_state.ingested_filename = uploaded_file.name
            logger.info(f"PDF file ingested successfully: {uploaded_file.name}")
            st.success("PDF uploaded successfully!")              # green success message

        except PipelineError as e:
            logger.error(f"Error in ingesting PDF file: {e}")
            st.error(f"Error in ingesting PDF file: {e}")  # Display error message to the user

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)  # Clean up the temporary file


if  st.session_state.pdf_ingested:
    question = st.text_input("Enter your question:")           # question input
    if st.button("Submit"):               # submit button
        with st.spinner("Processing..."):              # loading indicator
            try:
                answer = st.session_state.pipeline.query(question)  # Query the pipeline with the user's question
                st.markdown("### 💡 Answer")
                st.markdown(answer)
                logger.info(f"Answer generated successfully: {answer}")
                st.success("Answer generated successfully!")  # green success message
            except Exception as e:
                logger.error(f"Error in processing question: {e}")
                st.error(f"Error in processing question: {e}")  # Display error message to the user
    else: 
        st.info("Please enter a question and click Submit to get an answer.")  # info message when submit button is not clicked
else:
    st.info("Please upload a PDF file to start asking questions.")  # info message when PDF is not ingested