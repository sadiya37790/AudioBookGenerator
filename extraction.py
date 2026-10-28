import pdfplumber
import docx
import pytesseract
from PIL import Image

def extract_text(file):

    name = file.name.lower()

    if name.endswith(".pdf"):

        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()   # may return None for image-only pages
                if page_text:
                    text += page_text + "\n"
        return text

    elif name.endswith(".docx"):

        doc = docx.Document(file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

    elif name.endswith(".txt"):

        return file.read().decode("utf-8")

    elif name.endswith(("png","jpg","jpeg")):

        image = Image.open(file)
        return pytesseract.image_to_string(image)

    return ""