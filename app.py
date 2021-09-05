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

	### the query string ?result_per_page takes an int arg, can be passed through url
	if request.args.get('results_per_page') is not None:

		results_per_page=int(request.args.get('results_per_page'))
	else:
	### if result_per_page isnt given, use default 25
		results_per_page=25
	# Set the pagination configuration
	page = request.args.get('page', 1, type=int)

	users=github_users.query.paginate(page=page, per_page=results_per_page)
	return render_template('index.html', users=users)