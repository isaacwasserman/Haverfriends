import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("private-key.json")
firebase_admin.initialize_app(cred)
