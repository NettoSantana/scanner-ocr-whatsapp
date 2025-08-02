from flask import Flask, request
from separar_renomear import processar_pdf
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "API OCR rodando 101.1%"

@app.route("/bot", methods=["POST"])
def bot():
    msg = request.values.get("Body", "").strip().lower()
    num_media = int(request.values.get("NumMedia", 0))
    response = MessagingResponse()

    if num_media > 0:
        media_type = request.values.get("MediaContentType0", "")
        media_url = request.values.get("MediaUrl0", "")

        if "pdf" in media_type:
            # Faz o download do PDF
            pdf_data = requests.get(media_url).content
            with open("arquivo_recebido.pdf", "wb") as f:
                f.write(pdf_data)

            # Chama função OCR
            resultado = processar_pdf("arquivo_recebido.pdf")
            response.message(f"📄 OCR finalizado:\n{resultado}")
        else:
            response.message("⚠️ Envie um PDF, por favor.")
    elif "teste" in msg:
        response.message("👋 Olá! Envie um PDF para iniciarmos o OCR.")
    else:
        response.message("📌 Ainda não sei o que fazer com essa mensagem. Envie um PDF.")

    return str(response)

if __name__ == "__main__":
    app.run()
