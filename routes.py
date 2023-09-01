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


#new_post = Blog(body="Your blog content", Head="Your Blog Post Title", comments="Your comments here")
#new_post.save()