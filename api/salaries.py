import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User
import random
from __init__ import app, db, cors
import flask
from model.jobs import Job
from model.jobuser import JobUser
from urllib import parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User
import random
from __init__ import app, db, cors
import flask
from model.jobs import Job
from model.jobuser import JobUser
from urllib import parse
from urllib.parse import urlparse
from urllib.parse import parse_qs

salaries_api = Blueprint('salaries_api', __name__, url_prefix='/api/salaries')
api = Api(salaries_api)


import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User
import random
from __init__ import app, db, cors
import flask
from model.jobs import Job
from model.jobuser import JobUser
from urllib import parse
from urllib.parse import urlparse
from urllib.parse import parse_qs

salaries_api = Blueprint('salaries_api', __name__, url_prefix='/api/salaries')
api = Api(salaries_api)

class JobUserAPI:        
    class _Salaries(Resource):
        def get(self):
            salaries = Job.query.with_entities(Job.pay).order_by(Job.pay).all()  
            if salaries:
                json_ready = [salary.serialize() for salary in salaries]
                return jsonify(json_ready)
            else:
                return jsonify([])  


    api.add_resource(_Salaries, '/salaries')
    def iterate_users(self):
        users = User.query.all()
        for user in users:
            print(user.username) 
            
def select_users_by_status(self, status):
    users = User.query.filter_by(status=status).all()
    serialized_users = []
    for user in users:
        serialized_user = {
            "id": user.id,
            "pay": user.pay,
            "title": user.title,
            "field": user.field,
        }
        serialized_users.append(serialized_user)
    return serialized_users



job_user_api = JobUserAPI()
job_user_api.iterate_users()  
employer_users = job_user_api.select_users_by_status('Employer') 
print(employer_users)  

app.register_blueprint(salaries_api)

if __name__ == "__main__":
    app.run(debug=True)

