import sys, importlib.resources
class _PkgCompat:
    @staticmethod
    def resource_filename(package, resource):
        return str(importlib.resources.files(package).joinpath(resource))
sys.modules["pkg_resources"] = _PkgCompat()

import os, cv2
from fer import FER
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"
MUSIC_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music")
detector = FER()

EMOTION_MAP = {
    "happy": "happy", "sad": "sad", "angry": "angry",
    "neutral": "neutral", "surprise": "happy",
    "fear": "neutral", "disgust": "neutral"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if not file:
            return render_template("index.html", error="No image uploaded")

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        img = cv2.imread(filepath)
        results = detector.detect_emotions(img)
        os.remove(filepath)

        if not results:
            return render_template("index.html", error="No face detected!")

        emotion = max(results[0]["emotions"], key=results[0]["emotions"].get)
        folder = EMOTION_MAP.get(emotion, "neutral")
        folder_path = os.path.join(MUSIC_BASE, folder)

        songs = []
        if os.path.exists(folder_path):
            songs = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]

        return render_template("result.html", emotion=emotion, folder=folder, songs=songs)

    return render_template("index.html", error=None)

@app.route("/music/<folder>/<song>")
def serve_music(folder, song):
    return send_file(os.path.join(MUSIC_BASE, folder, song))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
