from flask import Flask, request, jsonify
import os
from separar_renomear import processar_pdf

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "API OCR rodando 101.1%"



@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nome de arquivo inválido"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, "documento.pdf")
    file.save(filepath)

    arquivos_gerados = processar_pdf(filepath)
    return jsonify({"status": "sucesso", "arquivos": arquivos_gerados}), 200

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
