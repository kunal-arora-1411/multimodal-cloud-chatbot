import os
import io
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Avoid hardcoding OS-specific cache path; use env if provided
if os.getenv("TRANSFORMERS_CACHE"):
    os.environ["TRANSFORMERS_CACHE"] = os.getenv("TRANSFORMERS_CACHE")

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(image, return_tensors="pt")

    # Fix 2: Use torch.no_grad() for inference
    with torch.no_grad():
        out = model.generate(**inputs)
    
    return processor.decode(out[0], skip_special_tokens=True)
