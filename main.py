from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
import json

# Отримуємо JSON-ключ із змінної середовища
firebase_key = os.environ.get("FIREBASE_KEY_JSON")

if not firebase_key:
    raise Exception("❌ FIREBASE_KEY_JSON не знайдено!")

# Ініціалізуємо Firebase з рядка JSON
cred = credentials.Certificate(json.loads(firebase_key))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask API
app = Flask(__name__)

@app.route("/random-excuse", methods=["GET"])
def random_excuse():
    excuses_ref = db.collection("excuses").stream()
    excuses = [doc.to_dict() for doc in excuses_ref]
    if not excuses:
        return jsonify({"error": "Немає відмазок 😢"}), 404
    return jsonify(random.choice(excuses))

if __name__ == "__main__":
    print("🚀 API запускається на Railway...")
    # Для локального запуску: http://localhost:5000
    # Для Railway — слухає на 0.0.0.0 з портом із оточення
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
