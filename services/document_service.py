"""PDF ingestion and text extraction."""

from pypdf import PdfReader
from langchain_core.documents import Document


def extract_pdf_documents(uploaded_file) -> list[Document]:
    """Extract readable text page-by-page so citations retain page numbers."""
    uploaded_file.seek(0)
    reader = PdfReader(uploaded_file)
    documents: list[Document] = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = (page.extract_text() or "").strip()
        if not page_text:
            continue

        documents.append(
            Document(
                page_content=page_text,
                metadata={
                    "source": uploaded_file.name,
                    "page": page_number,
                    "document_type": "uploaded PDF",
                },
            )
        )

    return documents
