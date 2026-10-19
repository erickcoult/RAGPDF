import os
import tempfile
from uuid import uuid4

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from main import function_embedding
from dotenv import load_dotenv

load_dotenv()

BASE_FOLDER = "base"
MAX_CHUNKS = 90


def create_db(pdf_bytes):
    document = load_document(pdf_bytes)
    chunks = split_chunks(document)
    
    if len(chunks) > MAX_CHUNKS:
        raise ValueError(
            "This PDF has too much text for the free demo. Please upload a shorter one."
        )
    return vectorize_chunks(chunks)


def load_document(pdf_bytes):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_file.write(pdf_bytes)
        temp_path = temp_file.name
 
    try:
        return PyPDFLoader(temp_path).load()
    finally:
        os.remove(temp_path)


def split_chunks(document):
    document_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True
    )

    return document_splitter.split_documents(document)



def vectorize_chunks(chunks):
    return Chroma.from_documents(
        chunks,
        function_embedding,
        collection_name=f"session_{uuid4().hex}",
    )

