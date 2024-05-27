import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User
import random
from __init__ import app, db, cors, mail
import flask
from model.jobs import Job
from model.applications import Application
from model.jobuser import JobUser
from urllib import parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
from flask_mail import Message

job_api = Blueprint('job_api', __name__,
                   url_prefix='/api/job')

api = Api(job_api)

# procedure that has qualification and jobid as parameters and returns freelancers that have the specific qualification for the job they applied to

'''
    *Same process for all if statements except it will return different users depending on the qualification and jobid*
    1. create a list using the set operation of all the user ids that match the applications queried in the databasee with matching qualification and jobid
    2. iterate over each user id in the set created in step 1 and query the user database for the corresponding user and add it to a list
    3. use the read method defined in the user class to return the details of each user in step 2 in readable form
'''


def filter_application_qualification(qualification, jobid):

    if qualification is None:
        applications = Application.query.filter_by(jobid = jobid).all()
        
        return jsonify([application.read() for application in applications])

    if qualification == 'PhD':
        users_id = set([application.userid for application in Application.query.filter_by(qualification = 'PhD', jobid = jobid).all()])
        users = [User.query.filter_by(id=user).first() for user in users_id]
        phd_users = [user.read() for user in users]
        
        return jsonify(phd_users)


    elif qualification == 'Masters':
        users_id = set([application.userid for application in Application.query.filter_by(qualification = 'Masters', jobid = jobid).all()])
        users = [User.query.filter_by(id=user).first() for user in users_id]
        masters_users = [user.read() for user in users]
    
        return jsonify(masters_users)
    
    elif qualification == 'Bachelors':
        users_id = set([application.userid for application in Application.query.filter_by(qualification = 'Bachelors', jobid = jobid).all()])
        users = [User.query.filter_by(id=user).first() for user in users_id]
        bachelors_users = [user.read() for user in users]
        
        return jsonify(bachelors_users)
    
    elif qualification == 'Associates':
        users_id = set([application.userid for application in Application.query.filter_by(qualification = 'Associates', jobid = jobid).all()])
        users = [User.query.filter_by(id=user).first() for user in users_id]
        associates_users = [user.read() for user in users]

        return jsonify(associates_users)

class JobAPI:       
    class _CRUD(Resource):
        # uses the auth_middleware function to check if JWT token of user and see if they are an employer
        @token_required("Employer")
        def post(self, current_user): 
            
            # get request as JSON
            body = request.get_json()
            
            # get necessary input fields that user filled out
            title = body.get('title')
            description = body.get('description')
            qualification = body.get('qualification')
            pay = body.get('pay')
            field = body.get('field')
            location = body.get('location')
            jobpostee = body.get('jobpostee')
    
            # create job object with the necessary input fields
            jo = Job(title=title, 
                      description=description,
                      qualification=qualification,
                      pay=pay,
                      field=field,
                      location=location,
                      jobpostee=jobpostee)

            # used defined create function/method to add job to database
            job = jo.create()
            
            # returns dictionary of job if succesful
            if job:
                return jsonify(jo.read())

            # will return 400 if unsuccesful
            return {'message': f'Processed {title}, either a format error or User ID {description} is duplicate'}, 400

        # will return specific job if an id is passed in the url parameters of the request
        def get(self): 
            # get the query parameters of the request
            frontendrequest = request.url
            parsed_url = urlparse(frontendrequest)
            query_params = parse_qs(parsed_url.query)
            '''
            check if id is in the query parameters
            if it is, query the job database by the specific id and return the job
            if there is no id in the parameter, return all the jobs
            '''
            if 'id' in query_params:
                query_id = query_params['id'][0]
                job = Job.query.filter_by(id=query_id).first()
                if job:
                    return job.read()
                else:
                    return {'message': 'Job not found'}, 404
            else:
                jobs = Job.query.all()    
                json_ready = [job.read() for job in jobs]  
                return jsonify(json_ready) 

    class _updateJob(Resource):
        # put method that updates the details of the job
        def put(self):
            # query the job database by the specific id and get the first job object
            job = Job.query.filter_by(id=request.args.get("id")).first()
            
            # returns 404 if job isnt found
            if job is None:
                return {'message': f'Processed {request.args.get("id")}, unknown id'}, 404

            # get request as JSON
            body = request.get_json()
            # get necessary input fields that user filled out
            title = body.get('title')
            description = body.get('description')
            qualification = body.get('qualification')
            pay = body.get('pay')
            field = body.get('field')
            location = body.get('location')

            '''
            instead of creating a new job object, use the update method defined in the class of the job table
            and use the input fields that user filled out to update the details of the job
            '''
            updatedJob = job.update(title=title, description=description,qualification=qualification
                                    ,pay=pay, field=field,location=location,   )


            # returns dictionary of job if succesful
            if updatedJob:
                return jsonify(updatedJob.read())

            # will return 400 if unsuccesful
            return {'message': f'Processed {request.args.get("id")}, unknown id'}, 404

    class _viewApplication(Resource):
        # get method that will return the specific application
        def get(self):
            # query the application database and filter by the jobid and userid passed in the query parameters
            application = Application.query.filter_by(jobid=request.args.get('jobid'), userid=request.args.get('userid')).first()

            # return the first application found as a JSON dictionary
            return jsonify(application.read())  
        
                                                   
    
    class _editApplication(Resource):
        # put method that updates the details of the application
        def put(self):
            # query the application database and filter by the jobid and userid passed in the query parameters
            application = Application.query.filter_by(jobid=request.args.get('jobid'), userid=request.args.get('userid')).first()
            
            # get request as JSON
            body = request.get_json()
            # get necessary input fields that user filled out
            address = body.get('address')
            email = body.get('email')
            separationFactor = body.get('separationFactor')
            years_of_experience = body.get('years_of_experience')
        
            '''
            instead of creating a new application object, use the update method defined in the class of the application table
            and use the input fields that user filled out to update the details of the application
            '''
            updatedApplication = application.update(address=address, email=email,separationFactor=separationFactor, 
                                                    years_of_experience=years_of_experience
                                    )


            # returns dictionary of application if succesful
            if updatedApplication:
                return jsonify(application.read())

            # will return 400 if unsuccesful
            return {'message': f'Processed {updatedApplication}, format error'}, 400
    
    class _submitApplication(Resource):
        # post method that will add the application to the database
        def post(self):
            # get request as JSON
            body = request.get_json()
            
            # get necessary input fields that user filled out
            address = body.get('address')
            email = body.get('email')
            qualification = body.get('qualification')
            separationFactor = body.get('separationFactor')
            years_of_experience = body.get('years_of_experience')
            jobid = request.args.get('jobid')
            userid = request.args.get('userid')
    
            '''
            creates an application AND jobuser object to connect the application to the user that applied to the job
            '''
            ao = Application(userid=userid,
                             jobid=jobid,
                             address=address,
                             email=email,
                             qualification=qualification,
                             separationFactor=separationFactor,
                             years_of_experience=years_of_experience)


            juo = JobUser(jobid=jobid,
                          userid=userid)
            
            
            # used defined create function/method to add jobuser and application to database
            juo.create()
            application = ao.create()
            # returns dictionary of application if succesful
            if application:
                return jsonify(ao.read())

            # failure returns error
            return {'message': f'Processed {application}, either a format error or Application ID {application} is duplicate'}, 400
    
    class _applicationQualification(Resource):
        def get(self):
            qualification = request.args.get("qualification")
            jobid = request.args.get("jobid")
            return filter_application_qualification(qualification, jobid)
    class _applicationSortingAlgorithm(Resource):
        def get(self):
            job_id = request.args.get('id')
            applications = Application.query.filter_by(jobid=job_id).all()

            def bubble_sort_by_experience(applications):
                n = len(applications)
                for i in range(n):
                    for j in range(0, n-i-1):
                        if applications[j].years_of_experience < applications[j+1].years_of_experience:
                            applications[j], applications[j+1] = applications[j+1], applications[j]

            # Sort applications by years of experience in descending order
            bubble_sort_by_experience(applications)

            # Extract unique user IDs from the sorted applications
            users_id = set([application.userid for application in applications])
            
            # Retrieve users from the database
            users = [User.query.filter_by(id=user_id).first() for user_id in users_id]

            # Prepare the user-application list
            user_application_list = []
            for user in users:
                application = Application.query.filter_by(jobid=job_id, userid=user.id).first()
                user_application_list.append({
                    'user': user.read(),
                    'application': application.read()
                })

            return jsonify(user_application_list)

            
            
         
           
    # adds endpoints
    api.add_resource(_CRUD, '/')
    api.add_resource(_updateJob, '/updatejob')
    api.add_resource(_viewApplication, '/viewapplication')
    api.add_resource(_editApplication, '/editapplication')
    api.add_resource(_submitApplication, '/submitapplication')
    api.add_resource(_applicationQualification, '/applicationqualification')
    api.add_resource(_applicationSortingAlgorithm, '/applicationSortingAlgorithm')