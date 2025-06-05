from flask import Flask
from config import Config
from models.Database import db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database with the app
try:
    db.init_app(app)
except Exception as e:
    print(f"Database initialization failed: {e}")

