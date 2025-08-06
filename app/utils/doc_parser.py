### utils/doc_parser.py (Resume text extractor)
import PyPDF2
import docx
from io import BytesIO

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() for page in reader.pages if page.extract_text())

    elif file.name.endswith(".docx"):
        doc = docx.Document(BytesIO(file.read()))
        return " ".join([p.text for p in doc.paragraphs])

    return ""
