from flask import request, jsonify, Blueprint
from flask_restful import Api, Resource
from __init__ import app, db, cors
from model.surveys import Survey
from datetime import datetime

survey_api = Blueprint('survey_api', __name__, url_prefix='/api/survey')
api = Api(survey_api)

class SurveyAPI:
    class _CRUD(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            print(body) 
            
            independent = body['independent']
            artisticTalent = body['artisticTalent']
            communicationSkills = body['communicationSkills']
            fastTyper = body['fastTyper']
            handyPerson = body['handyPerson']
            problemSolving = body['problemSolving']
            showOff = body['showOff']
            teamPlayer = body['teamPlayer']
            
            job_suggested = suggest_job(independent, artisticTalent, communicationSkills, fastTyper, handyPerson, problemSolving, showOff, teamPlayer)
            print(job_suggested)
            survey = Survey(
                independent=independent,
                artisticTalent=artisticTalent,
                communicationSkills=communicationSkills,
                fastTyper=fastTyper,
                handyPerson = handyPerson,
                problemSolving = problemSolving,
                showOff = showOff,
                teamPlayer = teamPlayer,
                jobsuggested=job_suggested
            )
            survey = survey.create()
            
            if survey:
                return jsonify(survey.read())

            return {'message': f'Error processing request'}, 400
            
        def get(self):
            surveys = surveys.query.all()    # read/extract all users from database
            json_ready = [survey.read() for survey in surveys]  # prepare output in json
            return jsonify(json_ready) # j

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
def suggest_job(independent, artistic_talent, communication_skills, fastTyper, handy_person, problem_solving, show_off, team_player):
    job_suggested = "None"  

    # Conditions based on survey responses
    if independent == 'Yes' and artistic_talent == 'Yes':
        job_suggested = "Graphic Designer"
    elif artistic_talent == 'Yes' and communication_skills == 'Yes':
        job_suggested = "Multimedia Artist"
    elif fastTyper == 'Yes' and handy_person == 'Yes':
        job_suggested = "Virtual Assistant"
    elif problem_solving == 'Yes' and show_off == 'Yes':
        job_suggested = "Social Media Influencer"
    elif team_player == 'Yes' and communication_skills == 'Yes':
        job_suggested = "Public Relations Specialist"
    elif communication_skills == 'Yes':
        job_suggested = "Communications Specialist"
    elif fastTyper == 'Yes':
        job_suggested = "Data Entry Clerk"
    elif handy_person == 'Yes':
        job_suggested = "Maintenance Technician"
    elif problem_solving == 'Yes':
        job_suggested = "Problem Solver"
    elif show_off == 'Yes':
        job_suggested = "Salesperson"
    elif team_player == 'Yes':
        job_suggested = "Team Coordinator"
    
    return job_suggested

