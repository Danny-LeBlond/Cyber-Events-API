from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from flask import current_app
def get_db():
    return current_app.extensions['sqlalchemy'].db
db = SQLAlchemy()
def create_app():
    from pathlib import Path
    app = Flask("Cyber Events Web API",
                template_folder=Path(__file__).parent / "templates",
                static_folder=Path(__file__).parent / "static")
    app.secret_key = 'you-will-never-guess'
    from dotenv import load_dotenv
    load_dotenv()  
    app.config['TESTING'] = os.getenv("TESTING") == "1"
    print("Loaded RECAPTCHA_PUBLIC_KEY =", os.environ.get("RECAPTCHA_PUBLIC_KEY"))
    app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:135791@localhost:5432/cyber_events'
    db.init_app(app)
    with app.app_context():
        from api import models  
        from app import routes
    return app