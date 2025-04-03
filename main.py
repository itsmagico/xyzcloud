from flask import Flask, render_template, request, send_from_directory, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
MAX_STORAGE = 50 * 1024 * 1024 * 1024  # 50GB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "Nenhum arquivo enviado."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "Nome de arquivo inválido."}), 400

    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"status": "success", "message": "Arquivo enviado!"})

@app.route("/files")
def list_files():
    files = [{"name": f, "size": os.path.getsize(os.path.join(UPLOAD_FOLDER, f))} for f in os.listdir(UPLOAD_FOLDER)]
    return jsonify({"files": files})

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
