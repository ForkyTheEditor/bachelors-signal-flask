import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'how-about-you-just-try'
    FIREBASE_SECRET_KEY_PATH = 'signalship_secret_key.json'
    DB_URL = 'https://signalship-80e67-default-rtdb.europe-west1.firebasedatabase.app/'