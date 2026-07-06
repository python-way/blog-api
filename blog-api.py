from flask import Flask, request, jsonify
import datetime as dt

app = Flask(__name__)

posts = [
            {
              "id": 1,
              "title": "My First Blog Post",
              "content": "This is the content of my first blog post.",
              "category": "Technology",
              "tags": ["Tech", "Programming"],
              "createdAt": "2021-09-01T12:00:00Z",
              "updatedAt": "2021-09-01T12:00:00Z"
            }
        ]
        

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'title' not in data or 'content' not in data:
        return jsonify({
                    "error": "Missing required fields",
                    "required": ["title", "content"]
                }), 400

    new_post = {
                "id": max(post['id'] for post in posts) + 1 if posts else 1,
                "title": data['title'],
                "content": data['content'],
                "category": data['category'] if 'category' in data else None,
                "tags": data['tags'] if 'tags' in data else None,
                "createdAt": dt.datetime.now(),
                "updatedAt": dt.datetime.now()
            }

    posts.append(new_post)

    return jsonify(new_post), 201

@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()
    
    post = next((post for post in posts if post['id'] == post_id), None)

    if not post:
        return jsonify({"error": "Post does not exist"}), 404

    if not data:
        return jsonify({"error": "No data provided"}), 400
   
    post['title'] = data['title'] if 'title' in data else post['title']
    post['content'] = data['content'] if 'content' in data else post['content']
    post['updatedAt'] = dt.datetime.now()

    if 'category' in data:
        post['category'] = data['category']

    if 'tags' in data:
        post['tags'] = data['tags']
    

    return jsonify(post), 200

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)

    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    index = 0
    for i in range(0,len(posts)):
        if posts[i]['id'] == post_id:
            index = i
            break

    posts.pop(index)

    return jsonify({"message":"Post deleted successfully"}) , 204

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(post), 200

@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts), 200


if __name__ == "__main__":
    app.run(debug=True)
