"""Cached Google Gemini chat and embedding clients."""

import streamlit as st
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)


@st.cache_resource
def get_embeddings(model_name: str, api_key: str) -> GoogleGenerativeAIEmbeddings:
    """Create and cache the configured Gemini embeddings client."""
    return GoogleGenerativeAIEmbeddings(
        model=model_name,
        google_api_key=api_key,
    )


@st.cache_resource
def get_chat_model(model_name: str, api_key: str) -> ChatGoogleGenerativeAI:
    """Create and cache the configured Gemini chat model."""
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        api_key=api_key,
    )
