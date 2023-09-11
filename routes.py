from medblog import app, request, jsonify, db
from models import blog, Comment, Like

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
    valid_fields = ["head", "body", "user_id"]
    filtered_fields = {key:data[key] for key in valid_fields if key in data}

    new_post = blog(
        head= filtered_fields.get("head"),
        body= filtered_fields.get("body"),
        user_id = filtered_fields.get("user_id")
        )
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
    post = blog.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    post.delete()
    return jsonify({'message': 'Blog post deleted successfully'})

@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    blog_post = blog.query.get(post_id)

    if not blog_post:
        return jsonify({'message': 'Blog post not found'}), 404

    comment_text = data.get('text')
    user_id = data.get("user_id")

    if not comment_text:
        return jsonify({'message': 'Comment text is required'}), 400

    new_comment = Comment(text=comment_text, blog=blog_post, user_id=user_id)
    new_comment.save()
    return jsonify({'message': 'Comment created successfully'})

@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    blog_post = blog.query.get(post_id)

    if not blog_post:
        return jsonify({'message': 'Blog post not found'}), 404

    comments = [comment.serialize() for comment in blog_post.comments]
    return jsonify(comments)

@app.route('/api/posts/<int:post_id>/likes', methods=['POST'])
def create_like(post_id):
    data = request.get_json()
    blog_post = blog.query.get(post_id)

    if not blog_post:
        return jsonify({'message': 'Blog post not found'}), 404

    like = data.get('likes')
    user_id = data.get("user_id")

    if not like:
        return jsonify({'message': 'like text is required'}), 400
    if like != 1:
        return jsonify({"message":"No valid like"})

    new_like = Like(likes=like, blog=blog_post, user_id=user_id)
    new_like.save()
    all_likes = [like.serialize() for like in blog_post.likes]
    lenght_likes = len(all_likes)
    return jsonify({'message': 'like created successfully'}, lenght_likes)

#@app.route('/api/posts/<int:post_id>/likes', methods=['GET'])
#def get_comments(post_id):
    blog_post = blog.query.get(post_id)

    if not blog_post:
        return jsonify({'message': 'Blog post not found'}), 404

    #comments = [comment.serialize() for comment in blog_post.comments]
    return jsonify(comments)