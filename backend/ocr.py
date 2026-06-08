# ocr.py
import pytesseract
from PIL import Image
import re
import os

pytesseract.pytesseract.tesseract_cmd = os.getenv(
    "TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_text(image: Image.Image, lang="tel"):
    config = "--psm 6"
    return pytesseract.image_to_string(image, lang=lang, config=config)

def test(text: str):
    words = re.findall(r'\b\w+\b', text)
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    characters = len(text)
    avg_word_len = sum(len(w) for w in words) / len(words) if words else 0
    return {
        "characters": characters,
        "words": len(words),
        "sentences": len(sentences),
        "avg_word_len": avg_word_len,
    }
