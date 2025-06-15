from flask import Blueprint, render_template, request, redirect, url_for, session,flash
from .. import db
from ..models import User
from app.models import User,Employer,Jobseeker
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user


auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        if role == 'employer':
            company_name = request.form['company_name']
            employer = Employer(user_id=new_user.id, company_name=company_name)
            db.session.add(employer)

        elif role == 'jobseeker':
            full_name = request.form['full_name']
            jobseeker = Jobseeker(user_id=new_user.id, full_name=full_name)
            db.session.add(jobseeker)

        db.session.commit()
        flash('Registration successful!', 'success')
        login_user(new_user)
        return redirect(url_for('admin_user.dashboard'))  # Redirect to dashboard/homepage

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first() 
        if user and check_password_hash(user.password, password):
            print('if block.........')
            login_user(user) 
            return redirect(url_for('admin_user.dashboard'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.home'))