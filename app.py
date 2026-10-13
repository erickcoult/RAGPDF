import streamlit as st

def app():
    st.header("RAG Chat IA", divider=True)
    st.write("### Chat about what would you like to know about a PDF")

    user_message = st.chat_input("Write here your message")

    if user_message: 
        if "messagens" in st.session_state:
            messagens = st.session_state["messagens"]
        else:
            messagens = []
            st.session_state["messagens"] = messagens

        #User Message
        messagens.append({"user": "user", "text": user_message})

        #IA Message
        messagens.append({"user": "assistant", "text": "OK"})

        
        for message in messagens:
         with st.chat_message(message["user"]):
            st.write(message["text"])

app()