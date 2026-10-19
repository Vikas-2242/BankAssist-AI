"""Sidebar controls for uploading, indexing, and clearing documents."""

import streamlit as st

from services.document_service import extract_pdf_documents
from services.rag_service import build_vector_store


def initialize_session_state() -> None:
    """Initialize per-session app state without loading default documents."""
    st.session_state.setdefault("raw_documents", [])
    st.session_state.setdefault("vector_store", None)
    st.session_state.setdefault("history", [])


def render_sidebar(api_key: str, embedding_model: str) -> None:
    """Render the sidebar and handle knowledge-base actions."""
    with st.sidebar:
        st.header("Knowledge base")
        unique_sources = {
            document.metadata.get("source", "Unknown")
            for document in st.session_state.raw_documents
        }
        st.write(f"Indexed source documents: **{len(unique_sources)}**")

        uploaded_files = st.file_uploader(
            "Add policy PDFs (text-based PDFs work best)",
            type=["pdf"],
            accept_multiple_files=True,
            key="policy_pdfs",
        )

        if st.button(
            "Index uploaded PDFs", type="primary", use_container_width=True
        ):
            if not uploaded_files:
                st.warning("Choose at least one PDF first.")
            else:
                try:
                    new_documents = []
                    with st.spinner(
                        "Extracting PDF text and building the search index…"
                    ):
                        for uploaded_file in uploaded_files:
                            new_documents.extend(
                                extract_pdf_documents(uploaded_file)
                            )

                        if not new_documents:
                            st.error(
                                "No readable text was extracted. The PDF may be scanned; "
                                "OCR is not included in this version."
                            )
                        else:
                            # Build the replacement index before changing the current one.
                            new_vector_store = build_vector_store(
                                new_documents, embedding_model, api_key
                            )
                            st.session_state.raw_documents = new_documents
                            st.session_state.vector_store = new_vector_store
                            # Avoid showing old answers after the index changes.
                            st.session_state.history = []
                            st.success(
                                f"Index ready. Indexed {len(uploaded_files)} PDF(s) "
                                f"with {len(new_documents)} readable pages."
                            )
                except Exception as exc:
                    st.error(f"Could not index the uploaded files: {exc}")

        if st.button("Clear knowledge base", use_container_width=True):
            st.session_state.raw_documents = []
            st.session_state.vector_store = None
            st.session_state.history = []
            st.success("Knowledge base cleared.")
            st.rerun()

        st.divider()
        st.caption(f"Embedding model: {embedding_model}")
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.history = []
            st.rerun()
