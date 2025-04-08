from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Server is running!"

@app.route('/upload', methods=['POST'])
def upload():
    raw_audio = request.data
    filename = request.headers.get('X-Filename', 'upload.mp3')
    safe_name = secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, safe_name)

    with open(file_path, 'wb') as f:
        f.write(raw_audio)

    return jsonify({"message": "File received", "filename": safe_name})

# ✅ THIS PART IS CRUCIAL
if __name__ == '__main__':
    app.run(debug=True)
