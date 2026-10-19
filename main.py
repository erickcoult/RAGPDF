from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

prompt_template = """
Answer the user's question:

{question}

Based on the following information:

{base_info}

If you don't know the answer, just say "I don't know" and don't try to make up an answer.
"""

function_embedding = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )
model = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash"
    )


def has_relevant_result(result):
    return len(result) > 0 and result[0][1] >= 0.4






def ask(question, db):
    

    result = db.similarity_search_with_relevance_scores(
        question,
        k=2
    )


    if not has_relevant_result(result):
            return "I couldn't find any relevant information to answer your question."
        
        

    text_results = []

    for document, score in result:
        text_results.append(document.page_content)

    base_info = "\n\n----\n\n".join(text_results)

    prompt = ChatPromptTemplate.from_template(prompt_template)

    prompt = prompt.invoke({
        "question": question,
        "base_info": base_info
    })

    text_result = model.invoke(prompt)

    return text_result.text