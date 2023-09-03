from medblog import app, SQLAlchemy, request, redirect, jsonify
from routes import *
from models import blog, Comment



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
