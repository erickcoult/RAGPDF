from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

FOLDER_BASE = "base"


def create_db():
    document = load_document()
    chunks = split_chunks(document)
    vectorize_chunks(chunks)


def load_document():
    loader = PyPDFDirectoryLoader(FOLDER_BASE)
    document = loader.load()
    return document


def split_chunks(document):
    document_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True
    )

    chunks = document_splitter.split_documents(document)

    print(len(chunks))

    return chunks


def vectorize_chunks(chunks):
    db= Chroma.from_documents(chunks, GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
), persist_directory="db")
    print("Database created successfully")


create_db()