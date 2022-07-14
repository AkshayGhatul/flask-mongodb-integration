from flask_login import LoginManager
from flask_mongoengine import MongoEngine

# Database setup
DB_USERNAME = "flask-social-media"
DB_PASSWORD = "flasksocialmedia"
DB_NAME = "social-media-data"
DB_HOST = "flask-social-media.g6pcdpb.mongodb.net"
DB_PORT = 27017

db = MongoEngine()

# Login manager setup
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message = "Please login to access website."
login_manager.login_message_category = "info"
