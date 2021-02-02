import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import exceptions
cred = credentials.Certificate("private-key.json")
firebase = firebase_admin.initialize_app(cred)