import os
import json
from flask import Flask, session, render_template, request, jsonify, make_response, url_for
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
	print(users)
	return render_template('index.html', users=users)


### API ENDPOINT

@app.route("/api/users/profiles", methods=['GET'])
def get_users():
	user_list = []

	if request.args.get('results_per_page') == 'None' or request.args.get('results_per_page') == None :
		results_per_page=25
		
	else:
		### retrieve query parameter from url 
		results_per_page=int(request.args.get('results_per_page'))

		

	page = request.args.get('page', 1, type=int)
	users=github_users.query.paginate(page=page, per_page=results_per_page)
	
	for user in users.items:
		user_dict={}
		user_dict['username']= user.username
		user_dict['git_id']=user.git_id
		user_dict['avatar_url']=user.avatar_url
		user_dict['url']=user.url
		user_dict['type']=user.user_type
		user_list.append(user_dict)

	### make_response with jsonified userlist and send nextpage link with response header for pagination

	response = make_response(jsonify({
		'users': user_list
		}),
	200,
	)
	response.headers["nextpage"] = f"http://127.0.0.1:5000/api/users/profiles?page={users.next_num}&results_per_page={request.args.get('results_per_page')}" 
		
	return response

