from flask import Flask, render_template, request, jsonify
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch, io, base64
import arabic_reshaper
from bidi.algorithm import get_display
import openai
from openai import OpenAI
import requests

KEY = ""
with open("./.key", "r") as f:
    KEY = f.read().strip()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=KEY
)

MODEL_ID = "MohamedRashad/arabic-large-nougat"

app = Flask(__name__)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model once
processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForVision2Seq.from_pretrained(MODEL_ID).to(device).eval()

def ocr_arabic_pil(image):
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        generated_ids = model.generate(**inputs, max_length=1024)
    text = processor.decode(generated_ids[0], skip_special_tokens=True)
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/paste", methods=["POST"])
def paste_image():
    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image data"}), 400

    # Decode base64 image
    header, encoded = data.split(",", 1)
    image_bytes = io.BytesIO(base64.b64decode(encoded))
    image = Image.open(image_bytes).convert("RGB")

    # OCR
    text = ocr_arabic_pil(image)
    print(text)

    # Return image as base64 to display
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()

    return jsonify({"image": img_str, "text": text})

if __name__ == "__main__":
    app.run(debug=True)
