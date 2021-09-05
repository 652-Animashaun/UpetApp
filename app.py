import os
import json
from flask import Flask, session, render_template, request, jsonify
from sqlalchemy import create_engine, exc
import json

from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///github_users.db"
db = SQLAlchemy(app)



@app.route("/")
def index():
	# Set the pagination configuration
	page = request.args.get('page', 1, type=int)

	users=github_users.query.paginate(page=page, per_page=25)
	return render_template('index.html', users=users)