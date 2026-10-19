"""Streamlit entry point for BankAssist AI."""

import streamlit as st

from config import get_settings
from ui.chat import render_chat
from ui.sidebar import initialize_session_state, render_sidebar


st.set_page_config(page_title="BankAssist AI", page_icon="🏦", layout="wide")

settings = get_settings()

st.title("🏦 BankAssist AI")
st.caption(
    "Banking policy assistant powered by Python, Google Gemini, LangChain, and RAG"
)
st.info(
    "Demo only: use fictional/sample policy documents. "
    "Do not upload real customer or confidential banking data."
)

if not settings.google_api_key:
    st.error(
        "GOOGLE_API_KEY is missing. Create a Gemini API key in Google AI Studio "
        "and add it to your local .env file or Azure App Service settings."
    )
    st.stop()

initialize_session_state()
render_sidebar(
    api_key=settings.google_api_key,
    embedding_model=settings.embedding_model,
)
render_chat(
    chat_model=settings.chat_model,
    api_key=settings.google_api_key,
)
