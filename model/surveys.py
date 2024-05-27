from datetime import datetime
from __init__ import db, app

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    independent = db.Column(db.String(255), nullable=False)
    communicationSkills = db.Column(db.String(255), nullable=False)
    problemSolving = db.Column(db.String(255), nullable=False)
    artisticTalent = db.Column(db.String(255), nullable=False)
    fastTyper = db.Column(db.String(255), nullable=False)
    handyPerson = db.Column(db.String(255), nullable=False)
    showOff = db.Column(db.String(255), nullable=False)
    teamPlayer = db.Column(db.String(255), nullable=False)
    jobsuggested = db.Column(db.String(255), nullable=False)
    
    def __init__(self,independent,communicationSkills,problemSolving,artisticTalent,fastTyper,handyPerson,showOff,teamPlayer,jobsuggested):
        self.independent = independent
        self.communicationSkills = communicationSkills
        self.problemSolving = problemSolving 
        self.artisticTalent = artisticTalent 
        self.fastTyper =  fastTyper
        self.handyPerson = handyPerson
        self.showOff = showOff
        self.teamPlayer = teamPlayer 
        self.jobsuggested = jobsuggested 
        

    def read(self):
        return {
            'id': self.id,
            'independent':self.independent,
            'communicationSkills': self.communicationSkills,
            'problemSolving' : self.problemSolving,
            'artisticTalent' : self.artisticTalent,
            'fastTyper' : self.fastTyper,
            'handyPerson' : self.handyPerson,
            'showOff' : self.showOff,
            'teamPlayer' : self.teamPlayer,
            'jobsuggested' : self.jobsuggested,
        }
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

def initSurveys():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        s1 = Survey(independent="independent",
                artisticTalent="artisticTalent",
                communicationSkills="communicationSkills",
                fastTyper="fastTyper",
                handyPerson = "handyPerson",
                problemSolving = "problemSolving",
                showOff = "showOff",
                teamPlayer = "teamPlayer",
                jobsuggested="jobsuggested"
                )
        
        try:
            s1.create()
        except Exception as e:
            print(f"Error creating review: {e}")
            db.session.rollback()