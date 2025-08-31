from faster_whisper import WhisperModel
from tempfile import NamedTemporaryFile

# Load model once
model = WhisperModel("base")

def speech_to_text(uploaded_file) -> str:
    # uploaded_file is of type streamlit.runtime.uploaded_file_manager.UploadedFile
    with NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        temp_audio.write(uploaded_file.read())  # ✅ This works only for UploadedFile, not raw bytes
        temp_audio_path = temp_audio.name

    segments, _ = model.transcribe(temp_audio_path)
    return " ".join([segment.text for segment in segments])
