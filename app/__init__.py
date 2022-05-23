import firebase_admin
from flask import Flask
from config import Config
from firebase_admin import credentials
from firebase_admin import db
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# Initialize config
app.config.from_object(Config)

# Initialize Firebase
cred = credentials.Certificate(app.config['FIREBASE_SECRET_KEY_PATH'])

firebase_admin.initialize_app(cred, {
    'databaseURL': app.config['DB_URL']
})

db_ref = db.reference()

# Initialize bootstrap
bootstrap = Bootstrap(app)

generated_signals_history = []
peaks_frequency_estimation = []

from app import routes
