import cv2
import pytesseract
import pandas as pd
import os

# ---------- TESSERACT PATH ----------
pytesseract.pytesseract.tesseract_cmd = r"C://Program Files//Tesseract-OCR//tesseract.exe"

# ---------- PATHS ----------
IMAGE_DIR = "images"
OUTPUT_FILE = "final_output.csv"

results = []

for image_name in os.listdir(IMAGE_DIR):
    image_path = os.path.join(IMAGE_DIR, image_name)
    image = cv2.imread(image_path)

    if image is None:
        continue

    # ---------- IMAGE PREPROCESSING ----------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # ---------- IMAGE CLARITY CHECK ----------
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    image_quality = "Clear" if blur_score > 100 else "Blurred"

    # ---------- OCR ----------
    extracted_text = pytesseract.image_to_string(
        thresh, config="--oem 3 --psm 6"
    )

    text_lower = extracted_text.lower()
    combined_text = text_lower + " " + image_name.lower()

    # ---------- SMART PRODUCT CLASSIFICATION ----------
    if any(word in combined_text for word in ["surf", "excel", "stain"]):
        product = "Surf Excel"
        category = "Detergents"

    elif any(word in combined_text for word in ["lays", "chips", "flavour"]):
        product = "Lays Chips"
        category = "Snacks"

    elif any(word in combined_text for word in ["dairy", "milk", "chocolate"]):
        product = "Dairy Milk"
        category = "Chocolates"

    elif any(word in combined_text for word in ["coca", "cola"]):
        product = "Coca Cola"
        category = "Beverages"

    elif any(word in combined_text for word in ["maggi", "noodles"]):
        product = "Maggi Noodles"
        category = "Instant Food"

    else:
        product = "Unknown"
        category = "Unknown"

    # ---------- SAVE RESULT ----------
    results.append({
        "image_name": image_name,
        "extracted_text": extracted_text.strip(),
        "image_quality": image_quality,
        "blur_score": round(blur_score, 2),
        "product": product,
        "category": category
    })

# ---------- SAVE CSV ----------
df = pd.DataFrame(results)
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Extraction completed successfully")
print(df)
