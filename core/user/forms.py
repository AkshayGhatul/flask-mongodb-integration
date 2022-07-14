import wtforms
from flask_wtf import FlaskForm
from wtforms import validators
from core.user.documents import User
from flask_wtf.file import FileAllowed
from core.upload_sets import PROFILE_PIC_SET

class UserRegistrationForm(FlaskForm):
    username = wtforms.StringField(validators=[validators.DataRequired(), validators.Length(max=30)])
    email = wtforms.EmailField(validators=[validators.DataRequired(), validators.Email(), validators.Length(max=100)])
    password = wtforms.StringField(validators=[validators.DataRequired()])
    confirm_password = wtforms.StringField(validators=[validators.DataRequired()])
    profile_pic = wtforms.FileField(validators=[FileAllowed(PROFILE_PIC_SET, 'Only images are allowed.')])

    def validate_email(self, email):
        if User.objects(email__iexact=email.data).first():
            raise validators.ValidationError("This email is already registered with us.")
        return True
    
    def validate(self):
        is_valid = FlaskForm.validate(self)
        password = self.password.data
        confirm_password = self.confirm_password.data
        if password and confirm_password:
            if password != confirm_password:
                self.password.errors += ("Two passwords does not match.",)
                return False
        if not is_valid:
            return False
        return True

class LoginForm(FlaskForm):
    email = wtforms.EmailField(validators=[validators.DataRequired(), validators.Email()])
    password = wtforms.StringField(validators=[validators.DataRequired()])

    def validate_email(self, email):
        if not User.objects(email__iexact=email.data).first():
            return False
        return True