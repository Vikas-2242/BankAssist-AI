"""Chat UI, suggested questions, and message history rendering."""

import streamlit as st

from services.rag_service import answer_question

SUGGESTED_QUESTIONS = [
    "What documents are needed to open a savings account?",
    "What does the policy say about reporting an unauthorized transaction?",
    "What are the minimum balance requirements?",
]


def _render_history() -> None:
    """Render saved messages and their retrieved evidence once."""
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("View retrieved evidence"):
                    for document in message["sources"]:
                        source = document.metadata.get("source", "Unknown source")
                        page = document.metadata.get("page", "N/A")
                        st.markdown(f"**{source}** · Page {page}")
                        st.write(document.page_content)


def render_chat(chat_model: str, api_key: str) -> None:
    """Render suggested questions and process chat input."""
    st.subheader("Ask the banking knowledge base")
    st.write("Choose a suggested question or ask about an indexed document.")

    columns = st.columns(len(SUGGESTED_QUESTIONS))
    for index, (column, example) in enumerate(zip(columns, SUGGESTED_QUESTIONS)):
        if column.button(
            example,
            key=f"suggested_question_{index}",
            use_container_width=True,
        ):
            st.session_state.pending_question = example

    _render_history()

    prompt = st.chat_input("Ask a question about the indexed banking documents…")
    if "pending_question" in st.session_state:
        prompt = st.session_state.pop("pending_question")

    if not prompt:
        return

    st.session_state.history.append({"role": "user", "content": prompt})

    if (
        st.session_state.vector_store is None
        or not st.session_state.raw_documents
    ):
        answer = (
            "No policy documents are indexed yet. Please upload one or more PDFs "
            "in the sidebar and click 'Index uploaded PDFs' before asking questions."
        )
        sources = []
    else:
        try:
            with st.spinner("Searching documents and drafting a cited answer…"):
                answer, sources = answer_question(
                    prompt,
                    st.session_state.vector_store,
                    chat_model,
                    api_key,
                )
        except Exception as exc:
            answer = f"Unable to answer the question. Details: {exc}"
            sources = []

    st.session_state.history.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
    # History is rendered only in _render_history(), avoiding duplicate messages.
    st.rerun()
