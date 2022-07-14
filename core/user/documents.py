from core import bcrypt
from io import BytesIO
from core.globals import db, login_manager
from core.choices import USERTYPES
from core.utilities.bcrypt_password import get_password_hash
from flask_login import UserMixin
from flask.helpers import send_file

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class User(UserMixin, db.Document):
    username = db.StringField(required=True, max_length=30)
    email = db.EmailField(required=True, unique=True, max_length=100)
    _password = db.BinaryField(required=True)
    usertype = db.StringField(max_length=5, choices=USERTYPES, required=True)
    profile_pic = db.ImageField()

    def set_password(self, password):
        self._password = get_password_hash(password)
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
    
    def is_actor(self):
        return self.usertype == "AC"

    def get_profile_pic(self):
        return self.profile_pic.read() if self.profile_pic else None

class TweetUser(db.DynamicDocument):
    user_id = db.DynamicField(unique=True)

class Tweet(db.DynamicDocument):
    user = db.ReferenceField(TweetUser, reverse_delete_rule=db.CASCADE)
