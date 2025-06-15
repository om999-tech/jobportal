from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_login import current_user
from app.models import User

class UserAdmin(ModelView):
    column_exclude_list = ['password']
    form_excluded_columns = ['applications']

    def on_model_change(self, form, model, is_created):
        if form.password.data and (is_created or model.password != form.password.data):
            model.password = generate_password_hash(form.password.data)
        return super().on_model_change(form, model, is_created)

    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.role == 'admin'


from flask_admin import Admin
from app.extensions import db
from app.models import User, Job, Application

def init_admin(app):
    admin = Admin(app, name='Job Portal Admin', template_mode='bootstrap4')
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(ModelView(Job, db.session))
    # admin.add_view(ModelView(Employer, db.session))
    admin.add_view(ModelView(Application, db.session))
