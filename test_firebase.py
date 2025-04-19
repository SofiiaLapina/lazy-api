import os
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ["PROJECT_ID"],
    "private_key_id": os.environ["PRIVATE_KEY_ID"],
    "private_key": os.environ["PRIVATE_KEY"].replace('\\n', '\n'),
    "client_email": os.environ["CLIENT_EMAIL"],
    "client_id": os.environ["CLIENT_ID"],
    "auth_uri": os.environ["AUTH_URI"],
    "token_uri": os.environ["TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["AUTH_PROVIDER_CERT"],
    "client_x509_cert_url": os.environ["CLIENT_CERT"]
})
firebase_admin.initialize_app(cred)

db = firestore.client()
excuses_ref = db.collection("excuses")
docs = excuses_ref.stream()

for doc in docs:
    print(doc.to_dict())