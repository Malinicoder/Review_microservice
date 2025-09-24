from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(45), nullable=True)
    rating = db.Column(db.Integer, nullable=False)   
    review_text = db.Column(db.Text, nullable=True)

