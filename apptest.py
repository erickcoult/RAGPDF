import streamlit as st
from main import ask

def app():
    st.header("RAG Chat IA", divider=True)
    st.write("### Chat about what would you like to know about a PDF")

    user_message = st.chat_input("Write here your message")
    

    if user_message:
        answer = ask(user_message)
        answer = answer.replace("$", r"\$")

        if "messagens" in st.session_state:
            messagens = st.session_state["messagens"]
        else:
            messagens = []
            st.session_state["messagens"] = messagens

        #User Message
        messagens.append({"user": "user", "text": user_message})

        #IA Message
        messagens.append({"user": "assistant", "text": answer})

        
        for message in messagens:
         with st.chat_message(message["user"]):
            st.write(message["text"])

app()