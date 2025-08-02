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
        pdf_path = "documento_recebido.pdf"
        try:
            # Baixar o PDF
            pdf_bytes = requests.get(media_url).content
            with open(pdf_path, "wb") as f:
                f.write(pdf_bytes)

            # Processar o PDF
            resultado = processar_pdf(pdf_path)

            # Responder com status + resultado
            msg = response.message()
            msg.body(f"✅ OCR finalizado com sucesso!\n\n{resultado}")
            os.remove(pdf_path)
        except Exception as e:
            response.message(f"❌ Erro ao processar o PDF: {str(e)}")

    elif "teste" in msg:
        response.message("👋 Olá! Envie um PDF para iniciarmos o OCR.")
    else:
        response.message("📌 Ainda não sei o que fazer com essa mensagem. Envie um PDF.")

    return str(response)

if __name__ == "__main__":
    app.run()
