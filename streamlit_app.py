import streamlit as st
from backend.rag_pipeline import get_rag_response
from backend.multimodal.caption_blip import generate_caption
from voice.speech_to_text import speech_to_text
from voice.text_to_speech import text_to_speech
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit page setup
st.set_page_config(page_title="🌩️ Multi-Cloud RAG Chatbot", layout="centered")
st.title("🤖 Multi-Cloud RAG Chatbot")
st.markdown("Ask anything about **AWS, Azure, or GCP** using text, image, or voice.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar input mode selector
mode = st.sidebar.radio("🎛️ Choose input mode:", ["Text", "Voice", "Image"])

query = None

# --- TEXT MODE ---
if mode == "Text":
    query = st.chat_input("💬 Ask your cloud question here...")

# --- VOICE MODE ---
elif mode == "Voice":
    st.info("🎤 Record your voice question below.")
    audio_file = st.file_uploader("Upload your voice (WAV/MP3)", type=["wav", "mp3"])
    if audio_file:
        with st.spinner("Transcribing voice..."):
            try:
                query = speech_to_text(audio_file)  # ✅ Read bytes
                st.success(f"🗣️ You said: {query}")
            except Exception as e:
                st.error(f"⚠️ STT Error: {str(e)}")

# --- IMAGE MODE ---
elif mode == "Image":
    img_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if img_file:
        with st.spinner("Generating caption..."):
            try:
                image_bytes = img_file.read()  # ✅ Read bytes from UploadedFile
                caption = generate_caption(image_bytes)
                query = f"see image: {caption}"
                st.image(img_file, caption=caption)
                st.success(f"🖼️ Image caption: {caption}")
            except Exception as e:
                st.error(f"⚠️ Image captioning error: {str(e)}")

# --- PROCESS QUERY ---
if query:
    # Save user query
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("⚡ Thinking..."):
        try:
            response = get_rag_response(query)
        except Exception as e:
            response = f"⚠️ Error in RAG pipeline: {str(e)}"

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Speak the response (voice mode)
    if mode == "Voice":
        try:
            audio_path = text_to_speech(response, "response.mp3")
            st.audio(audio_path, format="audio/mp3")
        except Exception as e:
            st.error(f"⚠️ TTS Error: {str(e)}")

# --- RENDER CHAT HISTORY ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
