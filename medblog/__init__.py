from flask import Flask, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///project.db"
db = SQLAlchemy(app)