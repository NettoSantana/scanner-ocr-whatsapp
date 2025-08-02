from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
from separar_renomear import processar_pdf

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "API OCR rodando 101.1%"

@app.route("/bot", methods=["POST"])
def bot():
    msg = request.values.get("Body", "").strip().lower()
    media_url = request.values.get("MediaUrl0", "")
    media_type = request.values.get("MediaContentType0", "")
    response = MessagingResponse()

    if media_type == "application/pdf" and media_url:
        # Etapa 1 – Aviso imediato
        response.message("🕐 Arquivo recebido. Iniciando OCR... Isso pode levar alguns segundos.")
        pdf_path = "documento_recebido.pdf"
        try:
            # Baixa o PDF
            pdf_bytes = requests.get(media_url).content
            with open(pdf_path, "wb") as f:
                f.write(pdf_bytes)

            # Processa o PDF
            resultado = processar_pdf(pdf_path)

            # Envia resultado
            follow_up = MessagingResponse()
            follow_up.message(f"✅ OCR finalizado!\n\n{resultado}")
            os.remove(pdf_path)
            return str(follow_up)
        except Exception as e:
            error = MessagingResponse()
            error.message(f"❌ Erro ao processar o PDF: {str(e)}")
            return str(error)

    elif "teste" in msg:
        response.message("👋 Olá! Envie um PDF para iniciarmos o OCR.")
    else:
        response.message("📌 Ainda não sei o que fazer com essa mensagem. Envie um PDF.")

    return str(response)

from waitress import serve

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)
