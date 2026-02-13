from pypdf import PdfReader
import docx
from config import MAX_CHARS


def limit_text(text):
    return text[:MAX_CHARS]


def read_pdf(path):

    try:
        reader = PdfReader(path)
        text = ""

        for page in reader.pages[:2]:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return limit_text(text)

    except:
        return ""


def read_docx(path):

    try:
        doc = docx.Document(path)
        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

            if len(text) >= MAX_CHARS:
                break

        return limit_text(text)

    except:
        return ""


def read_txt(path):

    try:
        with open(path, "r", encoding="utf-8") as f:
            return limit_text(f.read())
    except:
        return ""


def extract_content(path):

    if path.endswith(".pdf"):
        return read_pdf(path)

    if path.endswith(".docx"):
        return read_docx(path)

    if path.endswith(".txt") or path.endswith(".md"):
        return read_txt(path)

    return ""
