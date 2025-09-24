from flask import Blueprint, request, jsonify, g
from models import db, Review
import logging
from functools import wraps
import jwt

app1 = Blueprint("reviews", __name__)
JWT_SECRET = 'your_jwt_secret_key'
JWT_ALGORITHM = 'HS256'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            g.user_id = data.get('id')      
            g.user_role = data.get('role', 'user')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated


@app1.route("/add_reviews", methods=["POST"])
@token_required
def add_review():
    data = request.json
    try:
        product_id = data["product_id"]
        rating = data["rating"]
        review_text = data.get("review_text", "")

        new_review = Review(
            product_id=product_id,
            rating=rating,
            review_text=review_text,
            user_id=g.user_id 
        )
        db.session.add(new_review)
        db.session.commit()

        logging.info(f"Review added: product_id={product_id}, user_id={g.user_id}, rating={rating}")
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding review: {str(e)}")
        return jsonify({"error": "Failed to add review"}), 500


@app1.route("/reviews/<int:product_id>", methods=["GET"])
def get_reviews(product_id):
    try:
        reviews = Review.query.filter_by(product_id=product_id).all()
        response = [
            {
                "id": r.id,
                "rating": r.rating,
                "review_text": r.review_text,
                "user_id": r.user_id
            }
            for r in reviews
        ]

        logging.info(f"Fetched {len(reviews)} reviews for product_id={product_id}")
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Error fetching reviews: {str(e)}")
        return jsonify({"error": "Failed to fetch reviews"}), 500


@app1.route("/update_reviews/<int:review_id>", methods=["PUT"])
@token_required
def update_review(review_id):
    data = request.json
    try:
        review = Review.query.get_or_404(review_id)

        review.rating = data.get("rating", review.rating)
        review.review_text = data.get("review_text", review.review_text)
        db.session.commit()

        logging.info(f"Review updated: review_id={review_id}, user_id={g.user_id}")
        return jsonify({"message": "Review updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating review_id={review_id}: {str(e)}")
        return jsonify({"error": "Failed to update review"}), 500


@app1.route("/delete_reviews/<int:review_id>", methods=["DELETE"])
@token_required
def delete_review(review_id):
    try:
        review = Review.query.get_or_404(review_id)

        db.session.delete(review)
        db.session.commit()

        logging.info(f"Review deleted: review_id={review_id}, user_id={g.user_id}")
        return jsonify({"message": "Review deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting review_id={review_id}: {str(e)}")
        return jsonify({"error": "Failed to delete review"}), 500
