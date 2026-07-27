import PyPDF2
import re


def extract_text_from_file(file_path, filename):
    text = ""

    if filename.lower().endswith('.pdf'):
        text = extract_from_pdf(file_path)
    elif filename.lower().endswith('.txt'):
        text = extract_from_txt(file_path)

    return clean_text(text)


def extract_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text


def extract_from_txt(file_path):
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except Exception as e:
        print(f"TXT extraction error: {e}")
    return text


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', text)
    text = text.strip()
    return text


def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return sentences