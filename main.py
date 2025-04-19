from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
import json
from datetime import datetime
import requests

# Автоматичне визначення: локальний запуск чи Railway
if os.environ.get("RAILWAY_ENVIRONMENT"):
    print("🌩️ Режим: Railway (production)")
    firebase_key = os.environ.get("FIREBASE_KEY_JSON")
    if not firebase_key:
        raise Exception("❌ FIREBASE_KEY_JSON не знайдено в оточенні!")
    cred = credentials.Certificate(json.loads(firebase_key))
else:
    print("💻 Режим: локальний")
    with open("firebase-key.json") as f:
        firebase_key = json.load(f)
    cred = credentials.Certificate(firebase_key)

# Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask
app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random-excuse", methods=["GET"])
def random_excuse():
    # Отримання відмазок з Firestore
    excuses_ref = db.collection("excuses").get()
    excuses = [doc.to_dict() for doc in excuses_ref]
    if not excuses:
        return jsonify({"error": "Немає відмазок 😭"}), 404

    chosen = random.choice(excuses)
    client_ip = request.remote_addr or "unknown"
    log_entry = f"{datetime.now()} | {client_ip} | {chosen['text']}\n"

    # Локальний лог
    with open("excuse-log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

    # Надсилання логів на EC2
    try:
        requests.post("http://54.163.84.41:5000/log", json={
            "ip": client_ip,
            "text": chosen["text"]
        })
    except Exception as e:
        print("⚠️ Помилка надсилання логу на EC2:", e)

    # Рандомна гіфка з папки static/memes
    memes_dir = os.path.join(app.static_folder, "memes")
    if os.path.exists(memes_dir):
        meme_files = os.listdir(memes_dir)
        if meme_files:
            meme_url = f"/static/memes/{random.choice(meme_files)}"
        else:
            meme_url = ""
    else:
        meme_url = ""

    return jsonify({
        "text": chosen["text"],
        "meme_url": meme_url
    })

@app.route("/logs", methods=["GET"])
def show_logs():
    try:
        with open("excuse-log.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except FileNotFoundError:
        return "Файл логів не знайдено. Ще не було запитів або файл не створено."

if __name__ == "__main__":
    print("🚀 API запускається локально...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))