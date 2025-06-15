from flask import Blueprint, render_template, session, redirect, url_for,request
from ..models import Job,Employer,Jobseeker,User
from .. import db
from flask_login import current_user
from datetime import datetime, timedelta
from flask_login import login_required

adminuser_bp = Blueprint('admin_user', __name__, template_folder='templates')

@adminuser_bp.route('/dashboard')
@login_required
def dashboard():
    job_count = Job.query.count()
    all_job = Job.query.all()
    applied_job_ids = None
    if current_user.role == 'jobseeker':
        applied_job_ids = {a.job_id for a in current_user.jobseeker.applications}
    jobs = Job.query.filter_by(employer=current_user.employer).all()

    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = datetime(now.year, now.month, 1)
    year_start = datetime(now.year, 1, 1)

    stats = {
        "jobs_today": Job.query.filter(Job.posted_at >= today_start).count(),
        "jobs_week": Job.query.filter(Job.posted_at >= week_start).count(),
        "employers_total": Employer.query.count(),
        "employers_month": Employer.query.join(User).filter(User.role == 'employer', User.email != None, User.id != None, Employer.user_id == User.id, User.id != None, Employer.id != None, User.id != None, Employer.id != None, Employer.id != None, User.id != None).filter(User.id != None, User.id != None, User.id != None).filter(Employer.id != None).count(),  # Optional
        "jobseekers_total": Jobseeker.query.count(),
        "jobseekers_year": Jobseeker.query.join(User).filter(User.role == 'jobseeker', User.id != None).filter(Jobseeker.user_id == User.id).filter(User.id != None).filter(Jobseeker.id != None).filter(Jobseeker.id != None).filter(Jobseeker.id != None).count(),  # Optional
    }
    return render_template('dashboard.html', job_count=job_count,all_job=all_job,applied_job_ids=applied_job_ids,jobs=jobs,stats=stats)


#**********************Employer list******************

@adminuser_bp.route('/employers')
@login_required
def manage_employe():
    employers = Employer.query.options(db.joinedload(Employer.user)).all()
    return render_template('employer_list.html', employers=employers)

@adminuser_bp.route('/jobseekers')
@login_required
def manage_jobseeker():
    jobseekers = Jobseeker.query.options(db.joinedload(Jobseeker.user)).all()
    return render_template('jobseeker.html',jobseekers=jobseekers)


#**************Update employer*************

@adminuser_bp.route('/update_employer', methods=['POST'])
@login_required
def update_employer():
    emp_id = request.form.get('id')
    company_name = request.form.get('company_name')

    employer = Employer.query.get(emp_id)
    if employer:
        employer.company_name = company_name
        db.session.commit()
    
    return redirect(url_for('admin_user.manage_employe'))


#**************Delete employer*************
@adminuser_bp.route('/delete_employer/<int:id>', methods=['POST'])
@login_required
def delete_employer(id):
    employer = Employer.query.get(id)
    if employer:
        db.session.delete(employer)
        db.session.commit()
    return redirect(url_for('admin_user.manage_employe'))

#**************Update jobseeker*************
@adminuser_bp.route('/update_jobseeker', methods=['POST'])
@login_required
def update_jobseeker():
    js_id = request.form.get('id')
    full_name = request.form.get('full_name')

    jobseeker = Jobseeker.query.get(js_id)
    if jobseeker:
        jobseeker.full_name = full_name
        db.session.commit()

    return redirect(url_for('admin_user.manage_jobseeker'))

#**************Delete jobseeker*************
@adminuser_bp.route('/delete_jobseeker/<int:id>', methods=['POST'])
@login_required
def delete_jobseeker(id):
    jobseeker = Jobseeker.query.get(id)
    if jobseeker:
        db.session.delete(jobseeker)
        db.session.commit()
    return redirect(url_for('admin_user.manage_jobseeker'))




