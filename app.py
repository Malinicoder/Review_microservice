from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db
from routes import app1
from config import Config
import logging, os, json
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("reviews")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/reviews.log")
fh.setLevel(logging.INFO)
logger.addHandler(fh)
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
app.register_blueprint(app1)
if __name__ == "__main__":
    app.run(debug=True, port=5100)
