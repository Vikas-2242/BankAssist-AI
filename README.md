# BankAssist AI — Streamlit Community Cloud Ready

A demo banking-policy RAG app using Python, Streamlit, Google Gemini, LangChain, and FAISS.

> Demo only. Use fictional/sample policy documents. Do not upload real customer or confidential banking information. A publicly shared Streamlit app may be accessible to anyone with its URL.

## Project structure

```text
bankassist_ai_streamlit_cloud/
├── app.py
├── config.py                 # Reads local .env or Streamlit Cloud secrets
├── services/
│   ├── model_service.py
│   ├── document_service.py
│   └── rag_service.py
├── ui/
│   ├── sidebar.py
│   └── chat.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run locally (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and add your real GOOGLE_API_KEY
streamlit run app.py
```

Never commit `.env` or any API key to GitHub. `.gitignore` excludes `.env`.

## Deploy to Streamlit Community Cloud

1. Create/sign in to a GitHub account.
2. Create a new repository, for example `bankassist-ai`. The source code can be public for an easier demo, but it must not contain secrets or real customer information.
3. Upload/push the contents of this project folder to the repository. Ensure `app.py`, `config.py`, `requirements.txt`, `services/`, and `ui/` are at the repository root (not nested an extra folder deep). Do **not** upload `.env` or `.venv`.
4. Open https://share.streamlit.io/ and sign in with GitHub. Click **Create app**.
5. Select your repository, branch (`main` in a typical setup), and main file path `app.py`.
6. In **Advanced settings**, choose Python 3.12 (or another supported version compatible with your tested dependencies).
7. In the **Secrets** box, add TOML values like the following, replacing the placeholder with your real API key:

   ```toml
   GOOGLE_API_KEY = "paste-your-real-gemini-api-key-here"
   GEMINI_CHAT_MODEL = "gemini-3.5-flash-lite"
   GEMINI_EMBEDDING_MODEL = "gemini-embedding-2"
   ```

8. Click **Deploy** and wait for the environment to build. The app reads these values through `st.secrets`; no API key is needed in the GitHub repository.
9. Open the generated `*.streamlit.app` URL. Upload the dummy banking PDFs and click **Index uploaded PDFs** before asking questions.

## Notes and troubleshooting

- The `requirements.txt` file must be in the repository root, or next to the entrypoint. Streamlit installs Python dependencies from this file during the build.
- If the build fails, open the app's **Manage app / Logs** view and copy the first actual error from the build/runtime logs.
- Gemini API usage limits still apply. If indexing fails, the embedding model may have reached its own quota.
- The uploaded PDFs and FAISS index are held in app session memory, not durable storage. You may need to upload/re-index PDFs after the app restarts or the session resets.
- The app is intended for a demo only. Do not upload confidential financial or personal data.
