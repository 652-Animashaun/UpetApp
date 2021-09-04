import requests, re
import sqlite3, csv, json
from sqlite3 import Error
import argparse



# sqlite db connection-creation func
def create_connection(db_file):
	conn = None 
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)

	return conn


def get_users(args):

	url = "https://api.github.com/users"

	# if shell arguments is not given get first 150 profiles
	if args.total is None:
		quotient = 150//100
		mod =150%100
		compiled = getNext(url, mod=mod, quotient=quotient)
		return compiled	

	# if the shell parameter is given
	######
	else:
		n = int(args.total)
		quotient = n//100
		mod =n%100
		compiled = getNext(url, mod=mod, quotient=quotient)
		# print(f"COMPILED: {compiled}")
		return compiled


def getNext(url, mod=0, quotient=0, payload={'per_page': 100}):

	# Initialize a dict to hold all collected user info

	com_data = {}



	if quotient < 1 :
		users = []
		try:
			new_response = requests.get(url, params=payload)
			data = new_response.json()

			for user in data[:mod]:
				count=0
				users.append(user)
				username = user['login']
				
				count += 1
				print(f"{count}:{user['id']}:{username}")
			com_data['users'] = users
			return com_data
		except requests.exceptions.ConnectionError:
			print('An exception has ocurred. Is your internet connected?')

	else:

		try:
			for i in range(1, quotient+1):

				new_response = requests.get(url, params=payload)
				print('Next Page>>>>')
				data = new_response.json()

				# Pagination: url is next page link from response header and pass as url again

				url = new_response.links["next"]["url"]
				for user in data:
					username = user['login']
					com_data[username] = username
					print(f"{user['id']}:{username}")
			if mod > 0:
				new_response = requests.get(url, params=payload)
				data = new_response.json()

				count=0
				for user in data[:mod]:
					username = user['login']
					com_data[username] = user
					count += 1
					print(f"{count}:{user['id']}:{username}")
			return com_data
		except requests.exceptions.ConnectionError:
			print('An exception has ocurred. Is your internet connected?')

def main():

	# shell argument <total> -t for number of users to seed config

	parser = argparse.ArgumentParser(description='Dark lane demo tapes')
	parser.add_argument('-t','--total', help='specify the number of users to seed',required=False)
	args = parser.parse_args()

	total_users = get_users(args)

	
	### uncomment below lines and set path to sqlite db to insert results

	# database = r"C:\Users\Muizz\Desktop\umba_test\stageone.db"
	# conn = create_connection(database)
	# c = conn.cursor()
	# c.execute("CREATE TABLE IF NOT EXISTS github_users(id integer PRIMARY KEY, username varchar NOT NULL, avatar_url varchar NOT NULL, type varchar NOT NULL, url varchar NOT NULL)")
	# for i 


	try:

		for user in total_users['users']:

			c.execute("INSERT INTO github_users (username, git_id, avatar_url, user_type, url) VALUES (:username, :git_id, :avatar_url, :user_type, :url)",
				{"username": user['login'], "git_id": user['id'], "avatar_url":user['avatar_url'], "user_type": user['type'], "url": user['url']})

			username = user['login']
			git_id = user['id']
			avatar_url = user['avatar_url']
			user_type = user['type']
			url = user['url']


			print(f"INSERT INTO github_users (id, username, git_id, avatar_url, user_type, url) VALUES ({username}--{git_id}--{user_type}--{avatar_url}--{url}) ")

	except TypeError as e:
		print(f" This call returned a none type. But we cant return NONE can we now? {e}")






if __name__ == '__main__':
	main()



# payload={'per_page': 100, 'since':0}
# getNext("https://api.github.com/users", payload={'per_page': 100, 'since':int(since)})