import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import os
import re

# Caminhos
PDF = "documento.pdf"
POPPLER = r"C:\Users\vlula\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT

# Cria pasta de saída
os.makedirs("documentos_processados", exist_ok=True)

# Carrega o PDF original
reader = PdfReader(PDF)

# Converte para imagens (OCR)
pages_images = convert_from_path(PDF, poppler_path=POPPLER)

for i, (pdf_page, img_page) in enumerate(zip(reader.pages, pages_images)):
    # OCR
    img_path = f"pagina_{i+1}.png"
    img_page.save(img_path, "PNG")
    texto = pytesseract.image_to_string(Image.open(img_path), lang='por')

    # Limpa o texto pra evitar erros de leitura
    texto_limpo = texto.replace("\n", " ").upper()

    # Extrair tipo de documento
    tipo = "DOC"
    if "NF" in texto_limpo or "NOTA FISCAL" in texto_limpo:
        tipo = "NF"
    elif "BOLETO" in texto_limpo:
        tipo = "BL"
    elif "CTE" in texto_limpo or "CONHECIMENTO DE TRANSPORTE" in texto_limpo:
        tipo = "CTE"

    # Extrair número do documento (6+ dígitos)
    match_numero = re.search(r"\b\d{6,}\b", texto_limpo)
    numero = match_numero.group(0) if match_numero else f"{i+1:03}"

    # Extrair “fornecedor” (primeira palavra com 5+ letras maiúsculas)
    match_nome = re.search(r"\b[A-Z]{5,}\b", texto_limpo)
    fornecedor = match_nome.group(0) if match_nome else f"FORNECEDOR_{i+1:03}"

    # Nome final do arquivo
    nome_arquivo = f"{fornecedor}_{tipo}_{numero}.pdf"

    # Criar novo PDF só com essa página
    writer = PdfWriter()
    writer.add_page(pdf_page)

    with open(os.path.join("documentos_processados", nome_arquivo), "wb") as f:
        writer.write(f)

    print(f"✅ Página {i+1} salva como: {nome_arquivo}")
