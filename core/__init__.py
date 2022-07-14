import os
from flask import Flask, Blueprint
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_uploads import configure_uploads
from core.upload_sets import PROFILE_PIC_SET
from core.globals import (login_manager, db,
                    DB_PASSWORD, DB_USERNAME, DB_NAME,
                    DB_HOST, DB_PORT)

app = Flask(__name__, static_folder="static", template_folder="templates")

app.secret_key = "7l[]'Jhj!&!&^!"

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')
configure_uploads(app, PROFILE_PIC_SET)

app.config['MAX_CONTENT_LENGTH'] = 20 * 1000 * 1000 # Max file size allowed 20MB

csrf = CSRFProtect(app)

bcrypt = Bcrypt(app)

# Initialize database
app.config["MONGODB_SETTINGS"] = [
    {
        "host": f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
        "port": 27017,
        "alias": "default",
    }
]

db.init_app(app)

# initialize login manager
login_manager.init_app(app)

# Register custom jinja template filters & cli commands
with app.app_context():
    from core.jinja_filters import *
    from core.cli_commands.migrate_db import * 
    from core.cli_commands.load_tweet_datasets import *

# Register view blueprints
from core.user.views import user_blueprint
from core.twitter.views import twitter_blueprint

app.register_blueprint(user_blueprint, url_prefix="/")
app.register_blueprint(twitter_blueprint, url_prefix='/twitter')