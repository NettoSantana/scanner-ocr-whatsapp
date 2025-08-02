from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from separar_renomear import processar_pdf
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "✅ API OCR rodando"

@app.route("/bot", methods=["POST"])
def bot():
    msg = request.values.get("Body", "").strip().lower()
    num_media = int(request.values.get("NumMedia", 0))
    response = MessagingResponse()

    if num_media > 0:
        media_url = request.values.get("MediaUrl0")
        media_type = request.values.get("MediaContentType0")

        if media_type == "application/pdf":
            try:
                os.makedirs("documentos", exist_ok=True)
                caminho = "documentos/entrada.pdf"
                r = requests.get(media_url)
                with open(caminho, "wb") as f:
                    f.write(r.content)

                # Envia mensagem de status enquanto processa
                response.message("📥 PDF recebido! Processando OCR... Aguarde a resposta.")
                resultado = processar_pdf(caminho)
                print("✅ OCR concluído:", resultado)
            except Exception as e:
                print("❌ Erro ao processar o PDF:", e)
                response.message("⚠️ Erro ao processar o PDF. Tente novamente.")
        else:
            response.message("❌ Arquivo não suportado. Envie um PDF.")
    elif "teste" in msg:
        response.message("👋 Teste ok! Envie um PDF para iniciarmos o OCR.")
    else:
        response.message("📌 Ainda não sei o que fazer com essa mensagem. Envie um PDF.")

    return str(response)

if __name__ == "__main__":
    app.run()
