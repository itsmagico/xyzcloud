from flask import Flask, request, send_file
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/wanted")
def gerar_wanted():
    avatar_url = request.args.get("avatar")

    if not avatar_url:
        return "Erro: forneça o parâmetro ?avatar=", 400

    # Abrir imagem base (cartaz WANTED)
    fundo = Image.open("1000267143.jpg").convert("RGBA")

    # Baixar e redimensionar avatar
    try:
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA").resize((300, 300))
    except:
        return "Erro ao carregar avatar.", 400

    # Inserir avatar no centro do quadrado do cartaz (ajustado manualmente)
    fundo.paste(avatar, (105, 190), avatar)

    # Exportar imagem
    buffer = BytesIO()
    fundo.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
