from flask import Flask, request, send_file
from PIL import Image
import requests
from io import BytesIO
import os

app = Flask(__name__)

@app.route("/wanted")
def gerar_wanted():
    avatar_url = request.args.get("avatar")

    if not avatar_url:
        return "Erro: forneça o parâmetro ?avatar=", 400

    try:
        fundo = Image.open("static/wanted.jpg").convert("RGBA")

        # Pega o avatar
        resposta = requests.get(avatar_url)
        avatar = Image.open(BytesIO(resposta.content)).convert("RGBA").resize((300, 300))

        # Coloca o avatar no centro do cartaz (ajuste conforme necessário)
        fundo.paste(avatar, (105, 190), avatar)

        buffer = BytesIO()
        fundo.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, mimetype="image/png")
    except Exception as e:
        return f"Erro ao gerar imagem: {e}", 500

@app.route("/")
def home():
    return "API Wanted Online - Dorrita Bot"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
