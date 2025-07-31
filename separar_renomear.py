import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import os
import re

# Caminhos fixos
POPPLER = r"/usr/bin"  # Railway vai rodar com poppler instalado no container Linux
TESSERACT = r"/usr/bin/tesseract"

pytesseract.pytesseract.tesseract_cmd = TESSERACT

def processar_pdf(caminho_pdf):
    documentos = []
    pasta_saida = "documentos_processados"
    os.makedirs(pasta_saida, exist_ok=True)

    reader = PdfReader(caminho_pdf)
    pages_images = convert_from_path(caminho_pdf, poppler_path=POPPLER)

    for i, (pdf_page, img_page) in enumerate(zip(reader.pages, pages_images)):
        img_path = f"pagina_{i+1}.png"
        img_page.save(img_path, "PNG")
        texto = pytesseract.image_to_string(Image.open(img_path), lang='por')

        texto_limpo = texto.replace("\n", " ").upper()

        tipo = "DOC"
        if "NF" in texto_limpo or "NOTA FISCAL" in texto_limpo:
            tipo = "NF"
        elif "BOLETO" in texto_limpo:
            tipo = "BL"
        elif "CTE" in texto_limpo or "CONHECIMENTO DE TRANSPORTE" in texto_limpo:
            tipo = "CTE"

        match_numero = re.search(r"\b\d{6,}\b", texto_limpo)
        numero = match_numero.group(0) if match_numero else f"{i+1:03}"

        match_nome = re.search(r"\b[A-Z]{5,}\b", texto_limpo)
        fornecedor = match_nome.group(0) if match_nome else f"FORNECEDOR_{i+1:03}"

        nome_arquivo = f"{fornecedor}_{tipo}_{numero}.pdf"
        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

        writer = PdfWriter()
        writer.add_page(pdf_page)
        with open(caminho_arquivo, "wb") as f:
            writer.write(f)

        documentos.append(nome_arquivo)

    return documentos
