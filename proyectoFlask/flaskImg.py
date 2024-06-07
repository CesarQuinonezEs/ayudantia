from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configuración del directorio donde se guardarán las imágenes subidas
UPLOAD_FOLDER = 'img_upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def upload_image():
    # Verifica si la solicitud contiene archivos
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Verifica si se seleccionó un archivo
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        # Guarda el archivo en el directorio especificado
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({"message": "File successfully uploaded", "file_path": file_path}), 200
    else:
        return jsonify({"error": "Allowed file types are not met"}), 400

if __name__ == '__main__':
    app.run(debug=True)