from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenf import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

#postgresql+psycopg2://postgres:postgres@localhost:5432/ada_books_development

def create_app(test_config=None):
    app = Flask(__name__)
    # DB Config
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.book import Book

    from .routes import books_bp
    app.register_blueprint(books_bp)


    return app 
