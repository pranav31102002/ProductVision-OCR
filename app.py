import streamlit as st
import cv2
import pytesseract
import pandas as pd
import numpy as np
from PIL import Image
import re

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Product OCR",
    page_icon="🧠",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main-title {
    font-size: 40px;
    font-weight: 800;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f8f9fa;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
.badge-clear {
    color: white;
    background-color: #28a745;
    padding: 5px 10px;
    border-radius: 8px;
}
.badge-blur {
    color: white;
    background-color: #dc3545;
    padding: 5px 10px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="main-title">🧠 Smart Product Recognition using OCR</div>', unsafe_allow_html=True)
st.write("📷 Upload product images → 📝 Extract text → 🛒 Identify product & category")

# ---------- TESSERACT PATH ----------
pytesseract.pytesseract.tesseract_cmd = r"C://Program Files//Tesseract-OCR//tesseract.exe"

# ---------- FUNCTION: CLEAN OCR TEXT ----------
def clean_text(text):
    """Remove unwanted characters and extra spaces"""
    text = re.sub(r"[^a-zA-Z0-9\s,.!?]", "", text)  # Keep letters, numbers, basic punctuation
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with single space
    return text.strip()

# ---------- FILE UPLOADER ----------
uploaded_files = st.file_uploader(
    "📤 Upload Product Images",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

results = []

if uploaded_files:
    st.divider()

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        img_np = np.array(image)

        st.subheader(f"📦 {uploaded_file.name}")

        col1, col2, col3 = st.columns([2, 2, 3])

        # ---------- ORIGINAL IMAGE ----------
        with col1:
            st.image(image, caption="Original Image", use_column_width=True)

        # ---------- IMAGE PREPROCESSING ----------
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        with col2:
            st.image(thresh, caption="Processed Image", use_column_width=True)

        # ---------- IMAGE QUALITY ----------
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        is_clear = blur_score > 100
        quality_badge = (
            '<span class="badge-clear">Clear Image</span>'
            if is_clear else
            '<span class="badge-blur">Blurred Image</span>'
        )

        # ---------- OCR & CLEAN TEXT ----------
        raw_text = pytesseract.image_to_string(thresh, config="--oem 3 --psm 6")
        extracted_text = clean_text(raw_text)
        combined_text = (extracted_text + uploaded_file.name).lower()

        # ---------- PRODUCT CLASSIFICATION ----------
        if any(w in combined_text for w in ["surf", "excel"]):
            product, category = "Surf Excel", "Detergents"
        elif any(w in combined_text for w in ["lays", "chips"]):
            product, category = "Lays Chips", "Snacks"
        elif any(w in combined_text for w in ["dairy", "milk"]):
            product, category = "Dairy Milk", "Chocolates"
        elif any(w in combined_text for w in ["coca", "cola"]):
            product, category = "Coca Cola", "Beverages"
        elif any(w in combined_text for w in ["maggi", "noodles"]):
            product, category = "Maggi Noodles", "Instant Food"
        else:
            product, category = "Unknown", "Unknown"

        # ---------- INFO CARD ----------
        with col3:
            st.markdown(f"""
            <div class="card">
            <b>📝 Extracted Text</b><br>
            <i>{extracted_text or "No text detected"}</i><br><br>

            <b>🔍 Image Quality</b><br>
            {quality_badge}<br><br>

            <b>📊 Blur Score:</b> {round(blur_score, 2)}<br>
            <b>🛒 Product:</b> {product}<br>
            <b>📦 Category:</b> {category}
            </div>
            """, unsafe_allow_html=True)

        results.append({
            "image_name": uploaded_file.name,
            "extracted_text": extracted_text,
            "image_quality": "Clear" if is_clear else "Blurred",
            "blur_score": round(blur_score, 2),
            "product": product,
            "category": category
        })

# ---------- FINAL TABLE & METRICS ----------
if results:
    st.divider()
    df = pd.DataFrame(results)

    col1, col2, col3 = st.columns(3)
    col1.metric("📷 Total Images", len(df))
    col2.metric("🟢 Clear Images", len(df[df["image_quality"] == "Clear"]))
    col3.metric("🛒 Products Detected", df["product"].nunique())  # ✅ Safe column access

    st.subheader("📊 Final Results Table")
    st.dataframe(df, use_container_width=True)

    # ---------- DOWNLOAD CSV ----------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV Report",
        csv,
        "final_output.csv",
        "text/csv"
    )

    st.success("✅ Processing Completed Successfully")
