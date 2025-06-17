from flask import Flask
from config import Config
from models.Database import db
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize the database with the app
try:
    db.init_app(app)
except Exception as e:
    print(f"Database initialization failed: {e}")

