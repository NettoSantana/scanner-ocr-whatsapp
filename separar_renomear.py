import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import os
import re

def extrair_dados(texto):
    # Extrai nome do fornecedor antes do CNPJ
    fornecedor_match = re.search(r"([A-Z\s]+)\nCNPJ", texto)
    numero_match = re.search(r"SÉRIE\s*\d+\s*(\d{3,6})", texto)
    tipo = "CTE" if "CTE" in texto.upper() else "DOC"

    fornecedor = fornecedor_match.group(1).strip().replace(" ", "_") if fornecedor_match else "Fornecedor"
    numero = numero_match.group(1).strip() if numero_match else "0000"

    return fornecedor, tipo, numero

def processar_pdf(caminho_pdf):
    output_paths = []
    pasta_saida = "paginas_renomeadas"
    os.makedirs(pasta_saida, exist_ok=True)

    # Caminho para o Poppler no seu Windows
    poppler_path = r"C:\Users\vlula\Downloads\Release-24.08.0-0\Library\bin"

    # Converte o PDF em imagens
    imagens = convert_from_path(caminho_pdf, poppler_path=poppler_path)

    for i, imagem in enumerate(imagens):
        texto = pytesseract.image_to_string(imagem)
        fornecedor, tipo, numero = extrair_dados(texto)
        nome_arquivo = f"{fornecedor}_{tipo}_{numero}.pdf"
        caminho_saida = os.path.join(pasta_saida, nome_arquivo)

        # Salva a página como PDF
        doc = fitz.open()
        doc.insert_pdf(fitz.open(caminho_pdf), from_page=i, to_page=i)
        doc.save(caminho_saida)
        doc.close()

        output_paths.append(caminho_saida)

    return output_paths
