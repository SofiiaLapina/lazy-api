from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
import json
from datetime import datetime
import requests

# 🔥 Ініціалізація Firebase
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

# 🚀 Flask
app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random-excuse", methods=["GET"])
def random_excuse():
    """🎲 Отримати рандомну відмазку та оновити її рейтинг"""
    excuses_ref = db.collection("excuses").get()
    excuses = [doc for doc in excuses_ref]
    if not excuses:
        return jsonify({"error": "Немає відмазок 😭"}), 404

    chosen_doc = random.choice(excuses)
    chosen_data = chosen_doc.to_dict()

    # 📈 Збільшити рейтинг вибраної відмазки
    try:
        chosen_doc.reference.update({
            "rating": firestore.Increment(1)
        })
    except Exception as e:
        print("⚠️ Помилка оновлення рейтингу:", e)

    # 📝 Логи запиту
    client_ip = request.remote_addr or "unknown"
    log_entry = f"{datetime.now()} | {client_ip} | {chosen_data['text']}\n"
    with open("excuse-log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

    # 🔗 Відправка логів на EC2
    try:
        requests.post("http://54.163.84.41:5000/log", json={
            "ip": client_ip,
            "text": chosen_data["text"]
        })
    except Exception as e:
        print("⚠️ EC2 лог помилка:", e)

    # 🎞️ Підбір гіфки, якщо текст не містить "боже"
    meme_url = ""
    if "боже" not in chosen_data["text"].lower():
        memes_dir = os.path.join(app.static_folder, "memes")
        if os.path.exists(memes_dir):
            gif_files = [f for f in os.listdir(memes_dir) if f.endswith(".gif")]
            if gif_files:
                selected = random.choice(gif_files)
                meme_url = f"/static/memes/{selected}"

    return jsonify({
        "text": chosen_data["text"],
        "meme_url": meme_url
    })

@app.route("/excuses-stats", methods=["GET"])
def excuses_stats():
    """📊 Отримати статистику: кількість і топ-5 відмазок"""
    try:
        excuses_ref = db.collection("excuses").get()
        excuses = [doc.to_dict() for doc in excuses_ref]

        total_excuses = len(excuses)
        top_excuses = sorted(excuses, key=lambda x: x.get('rating', 0), reverse=True)[:5]

        return jsonify({
            "total": total_excuses,
            "top": [excuse['text'] for excuse in top_excuses]
        })
    except Exception as e:
        print("⚠️ Помилка завантаження статистики:", e)
        return jsonify({"error": "Помилка сервера"}), 500

@app.route("/logs", methods=["GET"])
def show_logs():
    """📝 Перегляд локального файлу логів"""
    try:
        with open("excuse-log.txt", "r", encoding="utf-8") as f:
            return f"<pre>{f.read()}</pre>"
    except FileNotFoundError:
        return "Файл логів не знайдено."

# 🏁 Запуск локально
if __name__ == "__main__":
    print("🚀 API запускається локально...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))