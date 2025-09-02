# 🌩️ Multimodal Cloud RAG Chatbot

**Ask anything about AWS, Azure, or GCP using Text • Voice • Image.**

> Canva‑ready README you can paste into your repo or publish as a one‑pager.

---

## ✨ Highlights

* **RAG over your cloud knowledge** using FAISS + Sentence‑Transformers
* **GROQ Llama‑3.3‑70B** for high‑quality answers (via REST)
* **Modes:** Text chat · Voice input (Whisper) · Image caption → query (BLIP)
* **Streamlit UI** with a simple chat history

---

## 🏗️ Architecture (at a glance)

```
[User] ────────────────▶ Streamlit UI
   │                          │
   │  text / voice / image    │
   ▼                          ▼
Voice (Whisper)         Image (BLIP caption)
   │                          │
   └───────────► Query text ◄──┘
                           │
                     RAG Pipeline
                (FAISS + embeddings)
                           │
                     GROQ LLM (API)
                           │
                           ▼
                      Final Answer
```

---

## 📁 Project Structure (expected)

```
multimodal-cloud-chatbot/
├─ backend/
│  ├─ rag_pipeline.py           # FAISS retriever + GROQ client
│  └─ vectorstore/
│     ├─ index.faiss
│     └─ index.pkl              # place your built index here
│  └─ multimodal/
│     └─ caption_blip.py        # BLIP image captioning
├─ voice/
│  ├─ speech_to_text.py         # faster-whisper STT
│  └─ text_to_speech.py         # pyttsx3 TTS
├─ streamlit_app.py             # UI (Text/Voice/Image)
├─ requirements.txt             # runtime deps
└─ .env                         # GROQ_API_KEY=...
```

> If your repo uses a flat layout, either move files into these folders or adjust imports in `streamlit_app.py` accordingly.

---

## ⚙️ Prerequisites

* **Python 3.10+** (3.11 OK)
* **FFmpeg** (required for audio handling; e.g., `choco install ffmpeg` on Windows, `sudo apt-get install ffmpeg` on Ubuntu)
* **Git LFS (optional)** if you store large FAISS indexes in Git

---

## 🚀 Quickstart

1. **Clone & venv**

```bash
git clone https://github.com/kunal-arora-1411/multimodal-cloud-chatbot.git
cd multimodal-cloud-chatbot
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
# plus a few needed by the code
pip install requests faster-whisper sentence-transformers langchain-core langchain-community
```

> If you hit platform issues with `faster-whisper`, try `pip install --upgrade ctranslate2`.

3. **Environment variables**
   Create a `.env` file at the repo root:

```ini
GROQ_API_KEY=your_groq_key_here
```

4. **Prepare the vector store**
   Place your FAISS files under `backend/vectorstore/` as:

```
backend/vectorstore/index.faiss
backend/vectorstore/index.pkl
```

(See **Build/Update the Knowledge Base** below if you need to generate these files.)

5. **Run the app**

```bash
streamlit run streamlit_app.py
```

Open the URL shown by Streamlit.

---

## 🧠 Build/Update the Knowledge Base (FAISS)

Here’s a simple script you can use to index a folder of Markdown/PDF/TXT docs into FAISS.

```python
# tools/build_faiss.py
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

docs_dir = Path("docs")  # put your content here

# Load text & PDFs (extend as needed)
loaders = []
loaders.append(DirectoryLoader(str(docs_dir), glob="**/*.txt", loader_cls=TextLoader))
loaders.append(DirectoryLoader(str(docs_dir), glob="**/*.md", loader_cls=TextLoader))
loaders.append(DirectoryLoader(str(docs_dir), glob="**/*.pdf", loader_cls=PyPDFLoader))

all_docs = []
for L in loaders:
    all_docs.extend(L.load())

# Embeddings & FAISS index
emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vs = FAISS.from_documents(all_docs, emb)

out = Path("backend/vectorstore")
out.mkdir(parents=True, exist_ok=True)
vs.save_local(str(out), index_name="index")
print("Saved FAISS index to:", out)
```

Run it:

```bash
pip install pypdf  # if indexing PDFs
python tools/build_faiss.py
```

---

## 🖥️ Using the App

### 1) Text mode

* Choose **Text** in the sidebar → type your question.
* The app retrieves top-k chunks from FAISS and asks GROQ Llama‑3.3‑70B to answer with context.

### 2) Voice mode

* Choose **Voice** → upload MP3/WAV.
* Audio is transcribed with **faster‑whisper** and used as the query.
* The answer can be played back using **pyttsx3**.

### 3) Image mode

* Choose **Image** → upload PNG/JPG.
* A BLIP caption is generated and used as the query text.

---

## 🔐 Secrets & Config

* **GROQ\_API\_KEY** must be present in your `.env`.
* (Optional) **TRANSFORMERS\_CACHE** can be set for BLIP model caching. If you’re not on Windows, remove or change the path in `caption_blip.py`.

---

## 🧩 Key Components

* **RAG pipeline**: FAISS retriever + prompt builder + GROQ REST call
* **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
* **LLM**: `llama-3.3-70b-versatile` via `https://api.groq.com/openai/v1/chat/completions`
* **Image captioning**: `Salesforce/blip-image-captioning-base`
* **STT**: `faster-whisper` (Whisper ‘base’ model)
* **TTS**: `pyttsx3`

---

## 🧪 Local Tips

* **Big downloads** the first time (BLIP & Whisper). Use a stable network.
* **GPU is optional**. CPU will work but be slower for BLIP/Whisper.
* If hosting on Streamlit Cloud/HF Spaces, verify FFmpeg and the `faster-whisper` wheel availability.

---

## 🐛 Troubleshooting

* **`ModuleNotFoundError: sentence_transformers`** → `pip install sentence-transformers`
* **`ImportError: cannot import name 'get_rag_response'`** → Ensure folder layout matches imports in `streamlit_app.py` or fix the import path.
* **`Error in RAG pipeline: ...`** → Check `GROQ_API_KEY` and confirm your FAISS files exist under `backend/vectorstore/`.
* **STT errors** → Confirm FFmpeg is installed; try smaller files; upgrade `ctranslate2`.
* **BLIP cache path** on non‑Windows → edit or remove `TRANSFORMERS_CACHE` line in `caption_blip.py`.

---

## 🗺️ Roadmap

* Inline citations (sources) in answers
* Live cloud API lookups (AWS/Azure/GCP) for real‑time posture
* Better chunking + reranking (e.g., Cohere/RRF)
* Prompt‑guardrails & safety filters
* Dockerfile + CI for reproducible deploys

---

## 🙌 Acknowledgments

* LangChain, FAISS, HuggingFace, Salesforce BLIP, OpenAI Whisper (faster‑whisper), Streamlit, GROQ

---

## 📜 License

MIT (or add your preferred license)

---

## 📷 Optional: Add a Banner/Screenshots (for Canva)

* Hero banner with title + emoji
* 3 tiles showing **Text**, **Voice**, **Image** modes
* Simple flow diagram (from the ASCII above)

