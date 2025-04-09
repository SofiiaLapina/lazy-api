from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
import json
from datetime import datetime

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
app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random-excuse", methods=["GET"])
def random_excuse():
    excuses_ref = db.collection("excuses").stream()
    excuses = [doc.to_dict() for doc in excuses_ref]
    if not excuses:
        return jsonify({"error": "Немає відмазок 😢"}), 404

    chosen = random.choice(excuses)
    client_ip = request.remote_addr or "unknown"
    log_entry = f"{datetime.now()} | {client_ip} | {chosen['text']}\n"

    with open("excuse-log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

    return jsonify(chosen)

# маршрут для перегляду логів
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
