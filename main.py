'''
main.py code provided by teacher
'''

from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization


# setup APIs
from api.user import user_api # Blueprint import api definition
from api.message import message_api
from api.jobuser import jobuser_api
from api.review import review_api
from api.job import job_api

# database migrations
from model.users import initUsers
from model.reviews import initReviews
from model.applications import initApplications
from model.messages import initMessages
from model.jobs import initJobs
from model.jobuser import initJobsUsers

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(user_api) # register api routes
app.register_blueprint(message_api)
app.register_blueprint(job_api)
app.register_blueprint(jobuser_api)
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(review_api)

'''
with app.app_context():
    initUsers()
    initJobs()
    initJobsUsers()
'''

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")


@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")



@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://127.0.0.1:4100/joblyFrontend/', 'http://localhost:4100/joblyFrontend/', 
                          'http://127.0.0.1:4100/joblyFrontend/jobs/', 'http://localhost:4100/joblyFrontend/jobs/',
                          'http://127.0.0.1:4100']:
        cors._origins = allowed_origin

        
    

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data


@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initMessages()
    initReviews()
    initJobs()
    initJobsUsers()
    initApplications()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# this runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8064")