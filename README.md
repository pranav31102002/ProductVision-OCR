# 🧠 ProductVision-OCR

A sleek and interactive **Streamlit-based computer vision application** that extracts text from product images using **Tesseract OCR**, evaluates image clarity, and intelligently classifies products into categories through a clean and user-friendly dashboard.

---

## 🚀 Features

- 📷 Upload and preview multiple product images  
- 📝 Extract text from images using **Tesseract OCR**  
- 🧹 Clean noisy and unreadable OCR outputs  
- 🔍 Analyze image clarity using **Blur Score (Laplacian Variance)**  
- 🛒 Automatically classify products (Snacks, Detergents, Beverages, etc.)  
- 📊 Display results in an interactive table  
- ⬇️ Export extracted results as **CSV**  

---

## 🧰 Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenCV](https://opencv.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Pillow](https://python-pillow.org/)

---

## ⚙️ Install the Dependencies
- pip install streamlit opencv-python pytesseract pandas numpy pillow
  
---

## Launch the App
- streamlit run app.py OR python -m streamlit run app.py

---

## How It Works
- User uploads product images
- Images are preprocessed (grayscale, blurring, thresholding)
- OCR extracts text from images
- Extracted text is cleaned to remove noise
- Image clarity is evaluated using blur score
- Products are classified using keyword-based logic
- Results are visualized and exported as CSV

---

## Credits
- Built using Streamlit
- OCR Engine: Tesseract OCR
- Image Processing: OpenCV

```bash
pip install streamlit opencv-python pytesseract pandas numpy pillow
