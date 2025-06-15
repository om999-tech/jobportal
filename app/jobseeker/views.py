from flask import Blueprint, render_template, request, redirect, session, url_for
from ..models import Job
from .. import db
from flask_login import current_user, login_required
from app.models import Application

jobseeker_bp = Blueprint('jobseeker', __name__, url_prefix='/jobseeker', template_folder='templates')

@jobseeker_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'jobseeker': return redirect(url_for('auth.login'))
    jobs = Job.query.order_by(Job.posted_at.desc()).all()
    return render_template('jobseeker_dashboard.html', jobs=jobs)


@jobseeker_bp.route('/jobs')
@login_required
def all_jobs():
    jobs = Job.query.all()
    applied_job_ids = {a.job_id for a in current_user.jobseeker.applications}
    return render_template('job_board.html', jobs=jobs, applied_job_ids=applied_job_ids)



@jobseeker_bp.route('/apply/<int:job_id>',methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    if current_user.role != 'jobseeker':
        return redirect(url_for('home'))
    job = Job.query.get_or_404(job_id)
    application = Application(job=job, jobseeker=current_user.jobseeker)
    db.session.add(application)
    db.session.commit()
    return redirect(url_for('admin_user.dashboard'))



@jobseeker_bp.route('/my-applications')
@login_required
def my_applications():
    if current_user.role != 'jobseeker':
        return redirect(url_for('home'))
    apps = Application.query.filter_by(jobseeker=current_user.jobseeker).all()
    return render_template('my_applications.html', applications=apps)