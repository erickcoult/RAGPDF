from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


PATH_DB = "db"

prompt_template = """
Answer to the user's question:

{question}

based on the following information:

{base_info}

if you don't know the answer, just say "I don't know" and don't try to make up an answer.
"""

question = input("Enter your question: ")

function_embedding = function_embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)
db = Chroma(persist_directory=PATH_DB, embedding_function=function_embedding)

result = db.similarity_search_with_relevance_scores(question, k=3)
print (result)
print (len(result))