from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import librosa
import numpy as np
from db import get_connection  # ✅ Import the function from db.py

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_mfcc(file_path, n_mfcc=13):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    mfcc_mean = np.mean(mfcc, axis=1)
    return mfcc_mean.tolist()

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/upload', methods=['POST'])
def upload():
    raw_audio = request.data
    filename = request.headers.get('X-Filename', 'upload.mp3')
    safe_name = secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, safe_name)

    with open(file_path, 'wb') as f:
        f.write(raw_audio)

    try:
        mfcc_vector = extract_mfcc(file_path)

        # ✅ Use the imported function
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO songs (filename, mfcc) VALUES (%s, %s)",
                    (safe_name, mfcc_vector))
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

    return jsonify({
        "message": "File received",
        "filename": safe_name,
        "mfcc": mfcc_vector
    })

if __name__ == '__main__':
    app.run(debug=True)
