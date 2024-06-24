from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.ProductionConfig')
    # app.config.from_object('config.DevelopmentConfig')
    
    
    app.register_blueprint(main)
    return app
