from flask import Blueprint, render_template, request, redirect, session, url_for,flash
from ..models import Job
from .. import db
from app.models import User,Application
from flask_login import current_user,login_required


employer_bp = Blueprint('employer', __name__, url_prefix='/employer', template_folder='templates')

@employer_bp.route('/dashboard')
def dashboard():
    # if session.get('role') != 'employer': return redirect(url_for('auth.login'))
    userid = current_user.id
    employer = User.query.filter_by(id=userid).first()
    jobs = Job.query.filter_by(employer_id=employer.id).all()
    return render_template('dashboard.html', jobs=jobs)


@employer_bp.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'employer':
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        desc = request.form['description'].strip()
        employer = current_user.employer

        # Check if a job with the same title and description exists for this employer
        existing_job = Job.query.filter_by(title=title, description=desc, employer_id=employer.id).first()

        if existing_job:
            flash("A job with the same title and description already exists.", "warning")
            return redirect(url_for('employer.post_job'))

        # Create the job
        job = Job(title=title, description=desc, employer=employer)
        db.session.add(job)
        db.session.commit()
        flash("Job posted successfully!", "success")
        return redirect(url_for('employer.employer_jobs'))

    return render_template('post_job.html')


@employer_bp.route('/employer_jobs')
@login_required
def employer_jobs():
    if current_user.role == 'admin':
        jobs = Job.query.all()
    else:    
        jobs = Job.query.filter_by(employer=current_user.employer).all()
    
    return render_template('job_list.html', jobs=jobs)



@employer_bp.route('/job_applications/<int:job_id>')
@login_required
def job_applications(job_id):
    print('jobid>>>>>',job_id)
    job = Job.query.filter_by(id=job_id).first()
    print('job in job applocation>..',job)
    return render_template('applications.html', job=job,applications=job.applications)


@employer_bp.route('/applications/<int:job_id>')
def view_applications(job_id):
    if session.get('role') != 'employer': return redirect(url_for('auth.login'))
    applications = Application.query.filter_by(job_id=job_id).all()
    return render_template('view_applications.html', applications=applications)


@employer_bp.route('/job/update/<int:job_id>', methods=['POST'])
@login_required
def update_job(job_id):
    if current_user.role != 'employer':
        return redirect(url_for('home'))

    job = Job.query.get_or_404(job_id)

    # Ensure the job belongs to the current employer
    if job.employer_id != current_user.employer.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('employer.employer_jobs'))

    # Get updated data from form
    title = request.form.get('title')
    description = request.form.get('description')

    if not title or not description:
        flash("Title and description cannot be empty.", "warning")
        return redirect(url_for('employer.employer_jobs'))

    job.title = title
    job.description = description
    db.session.commit()

    flash("Job updated successfully!", "success")
    return redirect(url_for('employer.employer_jobs'))




@employer_bp.route('/job/delete/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    if current_user.role != 'employer':
        return redirect(url_for('home'))

    job = Job.query.get_or_404(job_id)

    # Ensure the job belongs to the current employer
    if job.employer_id != current_user.employer.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('employer.employer_jobs'))

    # Optional: delete related applications if needed
    # Application.query.filter_by(job_id=job.id).delete()

    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully!", "success")
    return redirect(url_for('employer.employer_jobs'))
