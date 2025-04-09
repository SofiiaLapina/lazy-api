from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import random

# Firebase init
print("🛠️ Ініціалізую Firebase...")
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
print("✅ Firebase підключено!")

# Flask init
app = Flask(__name__)

@app.route("/random-excuse", methods=["GET"])
def random_excuse():
    excuses_ref = db.collection("excuses").stream()
    excuses = [doc.to_dict() for doc in excuses_ref]
    if not excuses:
        return jsonify({"error": "Немає відмазок 😢"}), 404
    return jsonify(random.choice(excuses))

if __name__ == "__main__":
    print("🚀 API запускається на http://localhost:5000 ...")
    app.run(debug=True)
