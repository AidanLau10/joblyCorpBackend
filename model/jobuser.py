from datetime import date
from __init__ import app, db
from sqlalchemy.exc import IntegrityError


# join table between the users and jobs table that connects freelancers to the jobs they applied to and employers to the jobs they posted
class JobUser(db.Model):
    __tablename__ = 'jobsusers'  

    id = db.Column(db.Integer, primary_key=True)
    '''
    "Foreign keys to the users and jobs table link each user(freelancer or employer), to the job they posted or applied to
    '''
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    jobid = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    dateApplied = db.Column(db.Date)

    # constructor to initialize the data when the jobuser object is being made with proper attributes/parameters
    def __init__(self, jobid, userid, dateApplied=date.today()):
        self.jobid = jobid
        self.userid = userid
        self.dateApplied = dateApplied
    
    # function/method to create the jobuser object
    def create(self):
        try:

            db.session.add(self)  
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None
    
    # function/method that returns the details of the jobuser object in a dictionary
    def read(self):
        return {
            "id": self.id,
            "jobid": self.jobid,
            "userid": self.userid,
            "dateApplied": self.dateApplied,
        }
    
# function that initializes test data
def initJobsUsers():
    with app.app_context():
        db.create_all()
        jobs = [
            JobUser(jobid=1, userid=2, dateApplied=date(1847, 2, 11)),
            JobUser(jobid=2, userid=3, dateApplied=date(2024, 4, 12))
        ]
        for job in jobs:
            try:
                job.create()
            except IntegrityError:
                db.session.remove()
                print(f"Records exist, duplicate title, or error: {job.title}")

