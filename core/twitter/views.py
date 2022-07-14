from flask import (Blueprint, render_template,
                redirect, url_for, request, flash)

twitter_blueprint = Blueprint("twitter", __name__, template_folder="templates")