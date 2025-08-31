from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
import os
import requests
import json
from dotenv import load_dotenv

# Load env vars (Hugging Face token, etc.)
load_dotenv()

# Load retriever
def load_retriever():
    # Ensure the vectorstore files are present (download from release if configured)
    ensure_vectorstore()
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    base = Path(__file__).parent
    vs_path = base / "vectorstore"
    vectorstore = FAISS.load_local(
        str(vs_path),
        embeddings=embedding_model,
        index_name="index",
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever()

retriever = load_retriever()

# Prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful multi-cloud assistant.\n"
        "Use the following context to answer the question:\n\n"
        "{context}\n\n"
        "Question: {question}"
    )
)

# Load GROQ API key from env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"  # High-quality, production-ready

def call_groq_llm(prompt_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.3,
        "max_tokens": 512
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"GROQ API error: {response.status_code} - {response.text}")


def get_rag_response(question: str):
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join(doc.page_content for doc in docs[:3])
    final_prompt = prompt.format(context=context, question=question)
    response = call_groq_llm(final_prompt)
    return response
