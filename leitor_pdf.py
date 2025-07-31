import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Caminhos
PDF = "documento.pdf"
POPPLER = POPPLER = r"C:\Users\vlula\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configura o caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT

# Converte o PDF em imagens
pages = convert_from_path(PDF, poppler_path=POPPLER)

# Processa cada página
for i, page in enumerate(pages):
    img_path = f"pagina_{i+1}.png"
    page.save(img_path, "PNG")
    
    texto = pytesseract.image_to_string(Image.open(img_path), lang='eng')
    print(f"\n--- Página {i+1} ---\n{texto}")
