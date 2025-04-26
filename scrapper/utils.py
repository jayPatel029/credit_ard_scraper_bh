import json
import re
import fitz # PyMuPDF
import os

# class CreditCardData(TypedDict, total=False):
#     card_name: str
#     bank: Optional[str]
#     joining_fee: Optional[str]
#     annual_fee: Optional[str]
#     rewards: Optional[str]
#     cashback: Optional[str]
#     other_features: Optional[str]
#     source_url: Optional[str] 


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def save_to_json(data: list[dict], filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# fee str to int
def clean_fee(raw: str) -> str:
    raw = raw.strip().lower()
    if "free" in raw or "zero" in raw:
        return "0"
    match = re.search(r'\d+[,.\d]*', raw.replace(',', ''))
    return match.group(0) if match else raw


# normalize, rm spaces, lowercase, rm punctuationa
def normalize_name(name: str) -> str:
    return re.sub(r'\W+', '', name.lower())


def safe_get(d: dict, key: str) -> str:
    return d.get(key, "N/A").strip() or "N/A"
