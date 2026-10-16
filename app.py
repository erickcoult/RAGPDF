import streamlit as st
import time
from pathlib import Path
from main import ask
from main import db
from create_db import create_db

BASE_FOLDER= Path("base")

@st.cache_resource
def ensure_db():
    if not db.get()["ids"]:   # banco vazio? (os mesmos ids da outra explicação)
        create_db()


ensure_db()

def app():
    st.header("RAG Chat IA", divider=True)
    st.write("### Chat about what would you like to know about a PDF")


    if "dbsession" not in st.session_state:
        st.session_state["dbsession"] = []

    dbsession = st.session_state["dbsession"]       

    with st.sidebar:
         uploaded_file =st.file_uploader("Upload Document (max 1)", type="pdf", max_upload_size=50)
        
    if uploaded_file is not None and uploaded_file.name not in dbsession:
        BASE_FOLDER.mkdir(exist_ok=True)

        
        for file in BASE_FOLDER.iterdir():
            if file.is_file():
                file.unlink()
        file_path = Path("base") / uploaded_file.name

        with open(file_path, "wb") as file:
         file.write(uploaded_file.getbuffer())

        create_db()

        dbsession.append(uploaded_file.name)



    if "messagens" not in st.session_state:
        st.session_state["messagens"] = []

    messagens = st.session_state["messagens"]

    for message in messagens:
        with st.chat_message(message["user"]):
            st.write(message["text"])

    user_message = st.chat_input("Write here your message")

    if user_message:
        # User Message
        messagens.append({
            "user": "user",
            "text": user_message
        })

        with st.chat_message("user"):
            st.write(user_message)

        # IA Message
        with st.chat_message("assistant"):
            with st.spinner("Thinking...", show_time=True):
                answer = ask(user_message)
                if answer:
                 answer = answer.replace("$", r"\$")
                st.write(answer)

        messagens.append({
            "user": "assistant",
            "text": answer
        })


app()