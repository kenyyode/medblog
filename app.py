from medblog import app, SQLAlchemy, request, redirect, jsonify
from routes import *
from models import blog



if __name__ == "__main__":
    app.run(debug=True)
