# Multi-Cloud RAG Chatbot (Streamlit)

This repo contains a Streamlit app (`streamlit_app.py`) that provides a multi‑modal RAG chatbot (text, optional voice and image captioning).

Below are concise steps to publish it on GitHub and deploy on Streamlit Community Cloud so you can use it from anywhere.

## 1) Prepare the repo

- Ensure you do NOT commit secrets. Put API keys in environment variables or Streamlit Secrets.
- This repo already includes a `.gitignore` that excludes `venv/`, `__pycache__/`, and `.env`.
- If your RAG index lives under `backend/vectorstore/` and is required at runtime, keep it committed. If it’s large, consider rebuilding it at startup or hosting it elsewhere.

## 2) Dependencies

- The app reads dependencies from `requirements.txt`.
- For cloud‑friendliness, ensure it contains only what you use. Heavy or OS‑specific packages can break builds.
- Commonly needed for this app:
  - streamlit
  - python-dotenv
  - requests
  - langchain
  - langchain-community
  - sentence-transformers
  - faiss-cpu
  - transformers
  - torch (CPU)
  - pillow
  - faster-whisper (for STT) or remove voice mode
  - gTTS (for TTS) or remove voice mode

If your current `requirements.txt` differs, adjust accordingly before deploying.

## 3) Secrets / Environment variables

Set the following as environment variables (locally via `.env`, in Streamlit Cloud via Secrets):

- GROQ_API_KEY: API key for the LLM (Groq)
- Any other provider keys you use

Locally you can create an `.env` file:

```
GROQ_API_KEY=your_key_here
```

Do not commit `.env`.

## 4) Push to GitHub

From the project root:

```
# Initialize once
git init
git add .
git commit -m "Initial commit: Streamlit RAG chatbot"

# Create a new GitHub repo (on github.com) and copy its URL, then:
git remote add origin https://github.com/<your-username>/<your-repo>.git
git branch -M main
git push -u origin main
```

## 5) Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io/ and sign in with GitHub.
2. Click "New app" and select your repo, branch (e.g., `main`), and file path `streamlit_app.py`.
3. In "Advanced settings" or the app’s Settings → Secrets, add required secrets (e.g., `GROQ_API_KEY`). These become environment variables at runtime.
4. Click "Deploy". The app will build from `requirements.txt` and then start.

Tip: If build time is long or fails due to heavy models, temporarily disable image/voice modes or switch them to call hosted APIs instead of loading large models.

## 6) Notes on multimodal features

- Voice (STT/TTS):
  - `faster-whisper` is preferred on cloud; `openai-whisper` and `pyttsx3` often fail due to system dependencies.
  - `gTTS` works for TTS but needs outbound network.
- Image captioning (BLIP):
  - Loading `Salesforce/blip-image-captioning-base` downloads large weights (>1GB). This may exceed startup constraints on some hosts.
  - Consider smaller models, pre‑bundled weights, or a hosted captioning API.

## 7) Alternative hosting

- Hugging Face Spaces (Streamlit): simple, supports hardware options; add your `requirements.txt` and set the app file to `streamlit_app.py`.
- Render/Fly.io/DO: run a web service that executes `streamlit run streamlit_app.py` and exposes port 8501.

## 8) Local run

```
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Troubleshooting

- Build failing: Trim `requirements.txt` to only needed libs; remove `google-cloud-sdk` and OS‑specific packages.
- ImportError for `torch` or `sentence-transformers`: add them to `requirements.txt`.
- Vector index not found: ensure `backend/vectorstore/index.faiss` and `index.pkl` are present in the repo or rebuild at startup.
- Secrets missing: configure `GROQ_API_KEY` in Streamlit Secrets.

---

Want me to: (a) clean up `requirements.txt` for cloud, and (b) optionally make small code tweaks to disable heavy features on cloud by a flag? I can do that next.
