from flask import Flask, request
from separar_renomear import processar_pdf
from twilio.twiml.messaging_response import MessagingResponse
import os
from waitress import serve

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "API OCR rodando 101.1%"

@app.route("/bot", methods=["POST"])
def bot():
    msg = request.values.get("Body", "").strip().lower()
    response = MessagingResponse()

    if "teste" in msg:
        response.message("👋 Olá! Envie um PDF para iniciarmos o OCR.")
    else:
        response.message("📌 Ainda não sei o que fazer com essa mensagem. Envie um PDF.")

    return str(response)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
