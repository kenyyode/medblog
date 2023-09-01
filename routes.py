from medblog import app, request, jsonify, db
from models import blog

@app.route('/')
def hello_world():
    return jsonify(message="Welcome to my our blog's backend")

@app.route('/api/posts', methods=["GET"])
def get_all_posts():
    posts = blog.query.all()
    return jsonify([post.serialize() for post in posts])

@app.route('/api/posts', methods=["POST"])
def create_new_post():
    data = request.get_json()
    new_post = blog(**data)
    new_post.save()
    return jsonify({"message":"Your Post was successfully added"})


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = blog.query.get(post_id)
    if post:
        return jsonify(post.serialize())
    else:
        return jsonify({'message': 'Post not found'}), 404
    

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    post = blog.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    for key, value in data.items():
        setattr(post, key, value)
    post.save()
    return jsonify({'message': 'Blog post updated successfully'})

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = bloglog.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    post.delete()
    return jsonify({'message': 'Blog post deleted successfully'})
