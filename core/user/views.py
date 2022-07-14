from flask import (Blueprint, render_template,
                redirect, url_for, request, flash)
from core.user.forms import UserRegistrationForm, LoginForm
from core.user.documents import User
from core.twitter.documents import Tweet, TweetUser
from werkzeug.utils import secure_filename
from core.utilities.bcrypt_password import get_password_hash
from flask_login import (current_user, login_user,
                        login_required, logout_user)

user_blueprint = Blueprint("user", __name__, template_folder="templates")

@user_blueprint.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('user.login'))

@user_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    else:
        form = LoginForm()
        dest = request.args.get('next')
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.objects(email=form.email.data).first()
                if user.check_password(form.password.data):
                    login_user(user)
                    if dest:
                        try:
                            return redirect(dest)
                        except:
                            pass
                    return redirect(url_for('user.dashboard'))
            flash("Please enter correct email and password.", 'error')
        return render_template("login.html", form=form)

@user_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        try:
            form = UserRegistrationForm()
            if form.validate_on_submit():
                user = User(
                    email = form.email.data,
                    username = form.username.data,
                )
                profile_pic = form.profile_pic.data
                if profile_pic:
                    user.profile_pic.put(profile_pic, filename=secure_filename(profile_pic.filename))
                user._password = get_password_hash(form.password.data)
                user.save()
                flash("Verify your email address.", 'info')
                return {'title': 'Success!', "desc": 'Please check your inbox to verify email address.'}, 200
            return {'error': form.errors}, 400
        except:
            return {
                'error': "Please contact to technical team or try again after a while."
            }, 500

@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user_blueprint.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


