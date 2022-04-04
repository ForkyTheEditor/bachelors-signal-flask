import firebase_admin
from flask import Flask
from config import Config
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)
app.config.from_object(Config)
cred = credentials.Certificate(app.config['FIREBASE_SECRET_KEY_PATH'])

firebase_admin.initialize_app(cred, {
    'databaseURL': app.config['DB_URL']
})

db_ref = db.reference()

from app import routes
