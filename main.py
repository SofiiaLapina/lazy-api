from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
import json
from datetime import datetime
import requests

# 🔐 Ініціалізація Firebase залежно від середовища
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

firebase_admin.initialize_app(cred)
db = firestore.client()

# 🔧 Налаштування Flask
app = Flask(__name__, template_folder="templates", static_folder="static")

# 🌐 Головна сторінка
@app.route("/")
def home():
    return render_template("index.html")

# 🎲 API: віддати випадкову відмазку та мем
@app.route("/random-excuse", methods=["GET"])
def random_excuse():
    # 📥 Витяг з Firestore
    docs = db.collection("excuses").get()
    excuses = [doc.to_dict() for doc in docs]

    if not excuses:
        return jsonify({"error": "Немає відмазок 😭"}), 404

    chosen = random.choice(excuses)
    excuse_text = chosen.get("text", "Без відмазки 🥲")

    # 🧾 Логування
    client_ip = request.remote_addr or "unknown"
    log_entry = f"{datetime.now()} | {client_ip} | {excuse_text}\n"

    try:
        with open("excuse-log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print("⚠️ Локальний лог не записано:", e)

    try:
        requests.post("http://54.163.84.41:5000/log", json={
            "ip": client_ip,
            "text": excuse_text
        })
    except Exception as e:
        print("⚠️ EC2 лог не надіслано:", e)

    # 🖼️ Гіфка
    meme_url = ""
    memes_dir = os.path.join(app.static_folder, "memes")
    if os.path.exists(memes_dir):
        gif_files = [f for f in os.listdir(memes_dir) if f.endswith(".gif")]
        if gif_files:
            selected_gif = random.choice(gif_files)
            meme_url = f"/static/memes/{selected_gif}"

    return jsonify({
        "text": excuse_text,
        "meme_url": meme_url
    })

# 📄 Вивід логів
@app.route("/logs", methods=["GET"])
def show_logs():
    try:
        with open("excuse-log.txt", "r", encoding="utf-8") as f:
            return f"<pre>{f.read()}</pre>"
    except FileNotFoundError:
        return "Файл логів не знайдено 🫤"

# 🚀 Запуск локально
if __name__ == "__main__":
    print("🚀 API запускається локально...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))