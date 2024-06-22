import os

class Config:
    SECRET_KEY = os.getenv('STST')
    DEBUG = os.getenv('DEBUG', True)
    UPLOAD_FOLDER = 'static/audio'