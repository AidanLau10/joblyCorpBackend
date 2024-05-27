from .users import User
from .jobs import Job
from .jobuser import JobUser
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# application table that freelancers populate by applying to jobs
class Application(db.Model):
    __tablename__ = 'applications'

    
    id = db.Column(db.Integer, primary_key=True)
    '''
    "Foreign keys to the users and jobs table link each application to a specific job in the job table and to the user who applied for that job, 
    which connects users to jobs with their application 
    '''
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    jobid = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    address = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=False, nullable=False)
    qualification = db.Column(db.String(255), unique=False, nullable=False)
    years_of_experience = db.Column(db.Integer, unique=False, nullable=False)
    separationFactor = db.Column(db.String(255), unique=False, nullable=False)

    # constructor to initialize the data when the application object is being made with proper attributes/parameters
    def __init__(self, userid, jobid, address, email, qualification, years_of_experience, separationFactor):
        self.userid = userid
        self.jobid = jobid
        self.address = address
        self.email = email
        self.qualification = qualification
        self.years_of_experience = years_of_experience
        self.separationFactor = separationFactor
        
    # functio/method to update the details of the application object
    def update(self, address="", email="", qualification="", years_of_experience="", separationFactor=""):
        """only updates values with length"""
        if len(address) > 0:
            self.address = address    
        if len(email) > 0:
            self.email = email
        if len(qualification) > 0:
            self.qualification = qualification
        if len(years_of_experience) > 0:
            self.years_of_experience = years_of_experience
        if len(separationFactor) > 0:
            self.separationFactor = separationFactor
        db.session.commit()
        return self
    
    # function/method to create the application object
    def create(self):
        try:
     
            db.session.add(self)  
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # function/method that returns the details of the application object in a dictionary
    def read(self):
        return {
            "id": self.id,
            "userid": self.userid,
            "jobid": self.jobid,
            "address": self.address,
            "email": self.email,
            "qualification": self.qualification,
            "years_of_experience": self.years_of_experience,
            "separationFactor": self.separationFactor
        }

# function that initializes test data
def initApplications():
    with app.app_context():
        db.create_all()
        applications = [
            Application(userid = 2, jobid=1, address="16601 Nighthawk Ln", email="nighthawkcodingsociety1@gmail.com", qualification="PhD", years_of_experience=4, separationFactor="I am unique"),
            Application(userid = 4, jobid=2, address="16602 Nighthawk Ln", email="nighthawkcodingsociety2@gmail.com", qualification="Masters", years_of_experience=334, separationFactor="I am unique"),
            Application(userid = 4, jobid=3, address="16603 Nighthawk Ln", email="nighthawkcodingsociety3@gmail.com", qualification="Masters", years_of_experience=41, separationFactor="I am unique"),
            Application(userid = 4, jobid=4, address="16604 Nighthawk Ln", email="nighthawkcodingsociety4@gmail.com", qualification="Masters", years_of_experience=45, separationFactor="I am unique"),
            Application(userid = 4, jobid=1, address="16605 Nighthawk Ln", email="nighthawkcodingsociety5@gmail.com", qualification="Masters", years_of_experience=61, separationFactor="I am unique"),
            Application(userid = 5, jobid=2, address="16606 Nighthawk Ln", email="nighthawkcodingsociety6@gmail.com", qualification="Bachelors", years_of_experience=17, separationFactor="I am unique"),
            Application(userid = 5, jobid=3, address="16607 Nighthawk Ln", email="nighthawkcodingsociety7@gmail.com", qualification="Bachelors", years_of_experience=96, separationFactor="I am unique"),
            Application(userid = 5, jobid=1, address="16608 Nighthawk Ln", email="nighthawkcodingsociety8@gmail.com", qualification="Bachelors", years_of_experience=58, separationFactor="I am unique"),
            Application(userid = 6, jobid=4, address="16609 Nighthawk Ln", email="nighthawkcodingsociety9@gmail.com", qualification="Associates", years_of_experience=110, separationFactor="I am unique"),
            Application(userid = 6, jobid=1, address="16610 Nighthawk Ln", email="nighthawkcodingsociety10@gmail.com", qualification="Associates", years_of_experience=121, separationFactor="I am unique"),
        ]
        for application in applications:
            try:
                application.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate title, or error: {application.title}")