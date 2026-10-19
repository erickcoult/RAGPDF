import streamlit as st

from pypdf import PdfReader
from main import ask
from create_db import create_db

MAX_PAGES = 15



def app():
    st.header("RAG Chat AI", divider=True)
    st.write("### Ask anything about your PDF")
    st.warning(
        "Note: This project uses the free tier of Google’s Gemini 3.6 Flash. Responses may sometimes be incomplete or inaccurate. PDFs are limited to 15 pages, and requests may be temporarily blocked if usage limits are reached."
    )

    if "messages" not in st.session_state:
        st.session_state["messages"] = []


    with st.sidebar:
        uploaded_file = st.file_uploader(
            f"Upload one PDF (up to {MAX_PAGES} pages)", type="pdf", max_upload_size=10
        )

    if (
        uploaded_file is not None
        and uploaded_file.name != st.session_state.get("pdf_name")
    ):
        total_pages = len(PdfReader(uploaded_file).pages)
        if total_pages > MAX_PAGES:
            st.sidebar.error(
                f"This PDF has {total_pages} pages. Please upload one with up to {MAX_PAGES} pages."
            )
            st.stop()
 
        try:
            with st.spinner("Processing PDF..."):
                new_db = create_db(uploaded_file.getvalue())
        except ValueError as error:
            st.sidebar.error(str(error))
            st.stop()
        except Exception:
            st.sidebar.error(
                "Too many requests right now. Please wait a minute and try again."
            )
            st.stop()
 

        if "db" in st.session_state:
            st.session_state["db"].delete_collection()
 
        st.session_state["db"] = new_db
        st.session_state["pdf_name"] = uploaded_file.name
        st.session_state["messages"] = []
 
    has_pdf = "db" in st.session_state
 
    for message in st.session_state["messages"]:
        with st.chat_message(message["user"]):
            st.write(message["text"])
 
    if not has_pdf:
        st.info("Upload a PDF in the sidebar to start chatting.")
 
    user_message = st.chat_input("Write here your message", disabled=not has_pdf)
 
    if user_message:
        st.session_state["messages"].append({"user": "user", "text": user_message})
 
        with st.chat_message("user"):
            st.write(user_message)
 
        with st.chat_message("assistant"):
            with st.spinner("Thinking...", show_time=True):
                answer = ask(user_message, st.session_state["db"])
            answer = answer.replace("$", r"\$")
            st.write(answer)
 
        st.session_state["messages"].append({"user": "assistant", "text": answer})
 
 
app()
