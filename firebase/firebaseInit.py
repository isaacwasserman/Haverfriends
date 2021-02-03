import firebase_admin
from firebase_admin import credentials, auth, exceptions, storage, firestore
cred = credentials.Certificate("private-key.json")
firebase = firebase_admin.initialize_app(cred, {"storageBucket": "haverfriends-9b932.appspot.com"})