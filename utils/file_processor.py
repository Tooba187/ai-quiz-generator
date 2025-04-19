import pdfplumber
from docx import Document
import fitz  # PyMuPDF
import re

def extract_text_from_file(uploaded_file):
    """Extract text from PDF, DOCX, or plain text files."""
    text = ""
    
    if uploaded_file.name.endswith('.pdf'):
        # Method 1: Using pdfplumber
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        except:
            # Fallback to PyMuPDF if pdfplumber fails
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = "\n".join([page.get_text() for page in doc])
            
    elif uploaded_file.name.endswith('.docx'):
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        # Assume it's a text file
        text = uploaded_file.getvalue().decode("utf-8")
    
    # Clean up text
    text = re.sub(r'\s+', ' ', text).strip()
    return text
