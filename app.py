import os
import json
from flask import Flask, session, render_template, request, jsonify, make_response, url_for
from sqlalchemy import create_engine, exc, desc
from flask_migrate import Migrate
import json

from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///github_users.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)



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
	user_id={}

	if request.args.get('id') != None:
		
		users=github_users.query.filter(github_users.git_id==int(request.args.get('id')))
		for user in users:

			user_id['username']= user.username
			user_id['git_id']=user.git_id
			user_id['avatar_url']=user.avatar_url
			user_id['url']=user.url
			user_id['type']=user.user_type
		if len(user_id) >= 1:

			return jsonify({
				'user':user_id
				})
		else:
			return jsonify({
				"Error": "User does not exist in db"
				}), 401



	if request.args.get('username') != None:

		users=github_users.query.filter(github_users.username==request.args.get('username'))
		for user in users:

			user_id['username']= user.username
			user_id['git_id']=user.git_id
			user_id['avatar_url']=user.avatar_url
			user_id['url']=user.url
			user_id['type']=user.user_type
		if len(user_id) >= 1:

			return jsonify({
				'user':user_id
				})
		else:
			return jsonify({
				"Error": "User does not exist in db"
				}), 401



	if request.args.get('order_by') != None:
		order_by=(request.args.get('order_by')).strip()
		if order_by == 'git_id':
			page = request.args.get('page', 1, type=int)
			# users = session.query(github_users).order_by(desc(github_users.order_by)).paginate(page=page, per_page=results_per_page)
			users=github_users.query.order_by(github_users.git_id).paginate(page=page, per_page=25)

			for user in users.items:
				user_dict={}
				user_dict['username']= user.username
				user_dict['git_id']=user.git_id
				user_dict['avatar_url']=user.avatar_url
				user_dict['url']=user.url
				user_dict['type']=user.user_type
				user_list.append(user_dict)

			response = make_response(jsonify({
				'users': user_list
				}),
			200,
			)
			response.headers["nextpage"] = f"http://127.0.0.1:5000/api/users/profiles?page={users.next_num}&results_per_page={request.args.get('results_per_page')}" 	
			return response


		elif order_by=='type':
			page = request.args.get('page', 1, type=int)
			users=github_users.query.order_by(desc(github_users.user_type)).paginate(page=page, per_page=25)
			for user in users.items:
				user_dict={}
				user_dict['username']= user.username
				user_dict['git_id']=user.git_id
				user_dict['avatar_url']=user.avatar_url
				user_dict['url']=user.url
				user_dict['type']=user.user_type
				user_list.append(user_dict)

			response = make_response(jsonify({
				'users': user_list
				}),
			200,
			)
			response.headers["nextpage"] = f"http://127.0.0.1:5000/api/users/profiles?page={users.next_num}&results_per_page={request.args.get('results_per_page')}" 	
			return response
		else:
			return jsonify({
				"Error": "You can only order_by git_id or type"
				}), 401


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

