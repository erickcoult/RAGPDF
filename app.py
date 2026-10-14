import streamlit as st
from main import ask


def app():
    st.header("RAG Chat IA", divider=True)
    st.write("### Chat about what would you like to know about a PDF")

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
        answer = ask(user_message)

        if answer:
            answer = answer.replace("$", r"\$")

        messagens.append({
            "user": "assistant",
            "text": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)


app()