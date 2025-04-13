# setup_db.py
from app import app
from model import db

with app.app_context():
    # Drop all existing tables first
    db.drop_all()
    # Then create all tables
    db.create_all()
    print("Database recreated successfully!")