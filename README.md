# UpetApp
This application is built on Python 3.9+

### Starting the development environment

Pull request on the main branch of the repo

Create an env in your current directory run 
$ Python venv -m env

Activate the environment
$ env\scripts\activate

Run 
$ pip install -r requirements.txt

# Initialize Seed.py

This script executes an API call to endpoint https://api.github.com/users 
By default, it only gets the first 150 users.
It can take a shell command parameter $ py seed.py -t <number>. Which changes default above
Uncomment DB creation block of code to create and insert to an SQLite DB.
- git_id, 
- username, 
- avatar_url, 
- user_type, 
- URL 
Or just uncomment print(f"") statement to simulate DB insert

# Starting the UpetApp localhost

Run 
$ flask run

In the browser navigate to localhost:5000

The flask app has a single frontend route "/", the index page

# Pagination
Each page displays a default (25) number of users; their username, profile photo in a single page
This number can be set as a query parameter ?results_per_page=<pagination>

All user thumbnail links to the user's github profile.

Initialize db -
$ flask db init

Create migration file
$ flask db migrate

Migrate 
$ flask db upgrade

Note the DB is not populated yet, see seed.py below.

# API Doumentation

The API endpoint is 'localhost:5000/api/users/profiles'
It takes a GET request 
Can take one of the following query parameters:
- localhost:5000/api/users/profiles?page=<page>
- localhost:5000/api/users/profiles?result_per_page=<pagination>
- localhost:5000/api/users/profiles?order_by=<git_id|type>
- localhost:5000/api/users/profiles?username=<term>
- localhost:5000/api/users/profiles?id=<id>

To transverse the list of result pages in a RESTful way,  get nextpage link using response.headers['nextpage']
If no pagination value is given, the api uses default 25.


# Unittest

The test functions lives in api_test_pagination.py
The unit_t.py module contains test case classes
Run unit tests by executing the command
$ Python unit_t.py

This tests the main functions of seed.py and app.py

# ContainariDeployment

using Docker,AWS ECS & EC2 
Create image instance and run container
$ docker build -t app .

$ docker run -d --publish app 

log on to aws console IAM from command line

$ aws ecr get-login-password --regionYOUR REGION | docker login --username AWS --password-stdin YOUR ID.dkr.ecr.YOUR REGION.amazonaws.com

tag and push repo from docker to AWS ECR

$ docker tag IMAGE NAME:latest 138909220235.dkr.ecr.us-east-2.amazonaws.com/ECR REPO:latest

$ docker push 138909220235.dkr.ecr.us-east-2.amazonaws.com/ECR REPO:latest




