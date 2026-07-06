from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

import datetime as dt

app = Flask(__name__)

# Database file path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "site.db")

# SQLite configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Avoids warning

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    tags = db.Column(db.String(1000), nullable=True)

with app.app_context():
    db.create_all()

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "title and content are required"}), 400
    
    try:
        new_post = Post(title=data['title'], content=data['content'],
                        category= data['category'] if 'category' in data else None,
                        tags = data['tags'] if 'tags' in data else None)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"id":new_post.id, "title":new_post.title, "content":new_post.content}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    try:
        data = request.get_json()
        
        post = Post.query.get_or_404(post_id)

        if not data:
            return jsonify({"error": "No data provided"}), 400
       
        post.title = data['title'] if 'title' in data else post.title
        post.content = data['content'] if 'content' in data else post.content
        post.updatedAt = dt.datetime.now()

        if 'category' in data:
            post.category = data['category']

        if 'tags' in data:
            post.tags = data['tags']
        
        db.session.commit()
        
        return jsonify({"id":post.id, "title":post.title, "content":post.content}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message":"Post deleted successfully"}) , 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({"id": post.id, "title": post.title, "content": post.content}), 200

@app.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": post.id, "title": post.title, "content": post.content} for post in posts]), 200


if __name__ == "__main__":
    app.run(debug=True)
