from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.rag_pipeline import get_rag_response
from backend.multimodal.caption_blip import generate_caption

app = FastAPI(
    title="Multi-Cloud RAG Chatbot",
    description="RAG chatbot with multimodal and cloud API support",
    version="1.0"
)

# Optional: Enable CORS for web frontend integration (Streamlit/Gradio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Multi-Cloud RAG Chatbot API"}

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    """
    Text-based RAG query endpoint.
    """
    try:
        response = get_rag_response(question)
        return {"question": question, "response": response}
    except Exception as e:
        return {"error": str(e)}

@app.post("/image-query")
async def image_query(image: UploadFile = File(...)):
    """
    Image-based input using BLIP (image captioning).
    """
    try:
        image_data = await image.read()
        caption = generate_caption(image_data)
        response = get_rag_response(caption)
        return {
            "image_caption": caption,
            "response": response
        }
    except Exception as e:
        return {"error": str(e)}
