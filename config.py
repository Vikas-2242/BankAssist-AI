"""Application configuration loaded from local environment or Streamlit secrets."""

import os
from dataclasses import dataclass

import streamlit as st
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings required by the application."""

    google_api_key: str
    chat_model: str
    embedding_model: str


def _setting(name: str, default: str = "") -> str:
    """Read a setting from environment variables first, then Streamlit secrets.

    Environment variables support local .env development and other hosts.
    Streamlit secrets support deployment on Streamlit Community Cloud.
    """
    value = os.getenv(name, "").strip()
    if value:
        return value

    try:
        secret_value = st.secrets.get(name, default)
    except Exception:
        # Streamlit secrets may not exist during local development.
        secret_value = default

    return str(secret_value).strip()


def get_settings() -> Settings:
    """Load settings from .env or the hosting platform's secret store."""
    load_dotenv()
    return Settings(
        google_api_key=_setting("GOOGLE_API_KEY"),
        chat_model=_setting("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite"),
        embedding_model=_setting("GEMINI_EMBEDDING_MODEL", "gemini-embedding-2"),
    )
