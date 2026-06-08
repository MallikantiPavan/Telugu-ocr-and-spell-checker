# app.py
import streamlit as st
from PIL import Image
import os
import requests
os.environ["TESSERACT_CMD"] = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

url = "http://localhost:8000/ocr"

st.title("Tesseract OCR")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
select = st.selectbox("Select Language", ["tel", "eng"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=500)

    if st.button("Extract Text"):
        uploaded_file.seek(0)
        files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
        response = requests.post(url, files=files, data={"lang": select})

        if response.status_code == 200:
            data = response.json()
            text = data["text"]
            stats = data["stats"]
            st.subheader("Extracted Text")
            st.text_area("Extracted Text", value=text, height=200)
            st.subheader("Statistics")
            st.text_area("Statistics", value=stats, height=200)
            st.download_button("Download Text", text)
            st.download_button("Download Statistics", stats)

        else:
            st.error(f"Failed to extract text: {response.status_code}")
