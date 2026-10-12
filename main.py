from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


PATH_DB = "db"

prompt_template = """
Answer the user's question:

{question}

Based on the following information:

{base_info}

If you don't know the answer, just say "I don't know" and don't try to make up an answer.
"""


def ask():

    function_embedding = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    db = Chroma(
        persist_directory=PATH_DB,
        embedding_function=function_embedding
    )

    model = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash"
    )

    while True:
        question = input("Enter your question(or 'exit' to quit): ")

        if question.lower().strip() == "exit":
            print("Chat ended.")
            break

        result = db.similarity_search_with_relevance_scores(
            question,
            k=2
        )

        if len(result) == 0 or result[0][1] < 0.4:
            print(
                "I couldn't find any relevant information to answer your question."
            )
            continue

        text_results = []

        for document, score in result:
            text = document.page_content
            text_results.append(text)

        base_info = "\n\n----\n\n".join(text_results)

        prompt = ChatPromptTemplate.from_template(prompt_template)

        prompt = prompt.invoke({
            "question": question,
            "base_info": base_info
        })

        text_result = model.invoke(prompt)

        print("Answer:", text_result.text)


ask()