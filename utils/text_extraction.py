
import fitz  # PyMuPDF

def extract_text_bun(path_pdf):
    text = ""
    doc = fitz.open(path_pdf)
    for page in doc:
        text += page.get_text()
    return text
