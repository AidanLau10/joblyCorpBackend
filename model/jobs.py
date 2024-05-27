from .jobuser import JobUser
from __init__ import app, db
from sqlalchemy.exc import IntegrityError

# jobs table that employers populate by posting jobs
class Job(db.Model):
    __tablename__ = 'jobs' 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=False)
    field = db.Column(db.String(255), unique=False, nullable=False)
    location = db.Column(db.String(255), unique=False, nullable=False)
    qualification = db.Column(db.String(255), unique=False, nullable=False)
    pay = db.Column(db.Integer, unique=False, nullable=False)
    '''
    Has a foreign key to the users table because it keeps track of who posts the job
    '''
    jobpostee = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    jobs = db.relationship('JobUser', backref='jobs', uselist=True, lazy='dynamic')
    applications = db.relationship('Application', backref='jobs', uselist=True, lazy='dynamic')
    
    # constructor to initialize the data when the job object is being made with proper attributes/parameters
    def __init__(self, title, description, field, location, qualification, pay, jobpostee):
        self.title = title   
        self.description = description
        self.field = field
        self.location = location
        self.qualification = qualification
        self.pay = pay
        self.jobpostee = jobpostee
    
    # functio/method to update the details of the job object
    def update(self, title="", description="", field="", location="", qualification="", pay=""):
        """only updates values with length"""
        if len(title) > 0:
            self._title = title    
        if len(description) > 0:
            self._description = description
        if len(field) > 0:
            self._field = field
        if len(location) > 0:
            self._location = location
        if len(qualification) > 0:
            self._qualification = qualification
        if pay is not None:
            self._pay = pay
        db.session.commit()
        return self
    
    # function/method to create the job object
    def create(self):
        try:
            db.session.add(self)  
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None
        
    # function/method that returns the details of the job object in a dictionary
    def read(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "field": self.field,
            "location": self.location,
            "qualification": self.qualification,
            "pay": self.pay,
            "jobpostee": self.jobpostee
        }

# function that initializes test data
def initJobs():
    with app.app_context():
        jobs = [
            Job(title='Software Engineer', description='Proficient experience in Java', field="Software", qualification="Masters", location="Remote", pay=32, jobpostee=1),
            Job(title='Web Developer', description='Proficient experience in Node', qualification="Bachelors", field="Web", location="Remote", pay=30, jobpostee=2),
            Job(title='UX Designer', description='Proficient experience in React', qualification="Associates", field="Software", location="Remote", pay=25, jobpostee=3),
            Job(title='IT Technician', description='Proficient experience in computers', qualification="PhD", field="IT", location="On-site", pay=2, jobpostee=4)
        ]
        for job in jobs:
            try:
                job.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate title, or error: {job.title}")

if __name__ == '__main__':
    initJobs()