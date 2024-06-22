from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.ProductionConfig')

    # Register blueprints
    app.register_blueprint(main)

    # Initialize extensions if you have any
    # e.g., db.init_app(app), migrate.init_app(app, db)

    return app
