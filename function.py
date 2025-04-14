import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
import random

print("Function as a Service стартувала...")
firebase_key = os.environ.get("FIREBASE_KEY_JSON")
if not firebase_key:
    raise Exception("FIREBASE_KEY_JSON не знайдено в змінних середовища!")

cred = credentials.Certificate(json.loads(firebase_key))
firebase_admin.initialize_app(cred)

db = firestore.client()
excuses_ref = db.collection("excuses").stream()
excuses = [doc.to_dict() for doc in excuses_ref]

if not excuses:
    print("Відмазок немає в базі!")
else:
    excuse = random.choice(excuses)
    print("Випадкова відмазка:", excuse["text"])
