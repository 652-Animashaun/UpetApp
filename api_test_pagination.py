import requests, re
import sqlite3, csv, json
from sqlite3 import Error
import argparse

from seed import get_users


def pagination_test(pagination):
	url= 'http://127.0.0.1:5000/api/users/profiles'
	# url = response.headers['nextpage']
	payload = {'results_per_page':pagination}

	for i in range(1,3):

		new_response = requests.get(url, params=payload)
		
		new_url = f"{url}{new_response.headers['nextpage']}"
		print(new_url)

		data = new_response.json()
		if len(data['users']) == int(pagination):
			return True
		else:
			print(f"{len(data['users'])}")
			return False



def git_get_test(nusers):

	users = get_users(nusers)
	users = users['users']

	if len(users)==int(nusers):
		print(len(users))
		return True
	else:
		print(get_users(nusers))
		return False
