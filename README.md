# 🧰 Flask Job Portal

A web-based job portal built with Flask that supports registration, login, and role-based dashboards for employers and jobseekers. Employers can post jobs, and jobseekers can apply for them.

---

## 🚀 Features

- User registration with role selection (Employer or Jobseeker)
- Secure authentication with Flask-Login and hashed passwords
- Employer dashboard to manage job postings
- Jobseeker dashboard to view and apply for jobs
- Admin views for managing users (optional)
- Bootstrap 5 modern UI
- Editable modals for updating records
- Delete confirmation modals (not browser alerts)

---

## 📦 Tech Stack

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Bootstrap 5
- PostgreSQL

---

## 🛠️ Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/job-portal.git
cd job-portal

###Create a Virtual Environment
python -m venv venv
source venv/bin/activate   

###Install Dependencies
pip install -r requirements.txt


🛠️ Initialize database migrations (only once):

flask db init       # Creates migrations/ folder
flask db migrate -m "Initial migration"
flask db upgrade    # Applies schema to the database

▶️ Run the app:
python run.py

Open your browser:
http://localhost:5000

🛠️ Create an Admin User with Flask-Admin:

1. Visit the Flask-Admin dashboard:
http://localhost:5000/admin

2. Click on "User" > "Create"

3. Fill out the following:
    - Email: admin@example.com
    - Password: (hashed manually or set plain for dev only)
    - Role: admin

✅ You can now log in or manage users via:
   http://localhost:5000/admin    

