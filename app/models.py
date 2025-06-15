from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from app.extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20))  # 'employer' or 'jobseeker'
    employer = db.relationship('Employer', backref='user', uselist=False)
    jobseeker = db.relationship('Jobseeker', backref='user', uselist=False)

class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_name = db.Column(db.String(150))
    jobs = db.relationship('Job', backref='employer')

class Jobseeker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(150))
    applications = db.relationship('Application', backref='jobseeker')

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'))
    posted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    applications = db.relationship('Application', backref='job')

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('jobseeker.id'))
    status = db.Column(db.String(50), default='Applied')  # e.g. 'Applied', 'Reviewed', 'Selected'
    applied_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


