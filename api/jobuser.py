import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
from model.users import User
import random
from __init__ import app, db, cors
import flask
from model.applications import Application
from model.jobs import Job
from model.jobuser import JobUser
from urllib import parse
from urllib.parse import urlparse
from urllib.parse import parse_qs

jobuser_api = Blueprint('jobuser_api', __name__,
                   url_prefix='/api/jobuser')

api = Api(jobuser_api)

# procedure that returns the jobs that a user applied to if they're a freelancer 
# or the jobs that an user posted if they're an employer
def get_user_jobs(userid):
    # query the user table for the first user that matches the userid passed in the query parameters of the request
    user = User.query.filter_by(id=request.args.get("userid")).first()

    # returns error if user isn't found
    if user is None:
        return jsonify({"error": "User not found"})
    
    '''
    1. create a list using the set operation of all the job ids that match the jobusers queried in the databasee with matching userids 
    2. iterate over each job id in the set created in step 1 and query the job database for the corresponding job and add it to a list
    3. use the read method defined in the job class to return the details of each job in step 2 in readable form
    '''
    if user.status == "Freelancer":
        jobs_id = set([jobuser.jobid for jobuser in JobUser.query.filter_by(userid = userid).all()])
        jobs = [Job.query.filter_by(id = job).first() for job in jobs_id]
        return jsonify([job.read() for job in jobs])
    elif user.status == "Employer": # if user.status is employer
        '''
        if the user is an employer, query the job database for all jobs with the jobpostee that matches the userid in the query parameter of the request
        apply the read method defined in the job class to return the details of each job in the query above
        '''
        jobpostee = Job.query.filter_by(jobpostee=request.args.get("userid")).all()
        # get employer id, read all jobs they posted. posted from jobs
        return jsonify([job.read() for job in jobpostee])


class JobUserAPI:        
    class _ApplyCount(Resource):
        # get method that will return the number of users that applied to a specific job
        def get(self):
            # get the query parameters of the request
            frontendrequest = request.url
            parsed_url = urlparse(frontendrequest)
            query_params = parse_qs(parsed_url.query)
            '''
            if a job id is in the query parameters, count how how many jobuser objects match the jobid because each jobuser object is the amount of 
            times somebody has applied to the specific job
            '''
            if 'id' in query_params:
                query_id = query_params['id'][0]
                count = JobUser.query.filter_by(jobid=query_id).count()
                if count:
                    return jsonify(count)
                else:
                    return jsonify('0')
    
    class _Profile(Resource):
        # get method that returns the jobs that a user applied to if they're a freelancer 
        # or the jobs that an user posted if they're an employer
        def get(self):
            # gets the userid in the query parameters of the request and passes it into the procedure defined above
            userid = request.args.get("userid")
            return get_user_jobs(userid)
        
    class _whoApplied(Resource):
        # get method that will return all the users that applied to a job
        def get(self):
            '''
            1. create a list using the set operation of all the user ids that match the applications queried in the databasee with matching job ids
            2. iterate over each user id in the set created in step 1 and query the user database for the corresponding user and add it to a list
            3. use the read method defined in the user class to return the details of each user in step 2 in readable form
            '''
            users_id = set([application.userid for application in Application.query.filter_by(jobid = request.args.get("id")).all()])
            users = [User.query.filter_by(id = user).first() for user in users_id]
            user_application_list = []
            for user in users:
                application = Application.query.filter_by(jobid= request.args.get("id"), userid=user.id).first()
                user_application_list.append( 
                        {'user': user.read(),
                        'application': application.read()})
            
            
            return user_application_list
            
    
    class _userStatus(Resource):
        # get method that will return the status and nam e of a user
        def get(self):
            # query the user database for the first user that matches the userid
            user = User.query.filter_by(id=request.args.get("userid")).first()
            # returns error if user isnt found
            if user is None:
                return jsonify({"error": "User not found"})
            
            if user.status == "Freelancer":
                return {'status': 'Freelancer',
                    'name': f'{user._name}'}
             
            elif user.status == "Employer":
                return {'status': 'Employer',
                    'name': f'{user._name}'}
    

            
    # adds endpoints
    api.add_resource(_ApplyCount, '/applycount')
    api.add_resource(_Profile, '/profile')
    api.add_resource(_whoApplied, '/whoapplied')
    api.add_resource(_userStatus, '/userstatus')

    
    