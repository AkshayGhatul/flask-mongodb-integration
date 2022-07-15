from flask import (Blueprint, render_template,
                redirect, url_for, request, flash)
from flask_login import (current_user, login_required)
from .documents import TweetUser
from .utilities.twitter_users import TwitterUsersUtils

twitter_blueprint = Blueprint("twitter", __name__, template_folder="templates")

@twitter_blueprint.route("/", endpoint='tweets')
@twitter_blueprint.route("/tweets", endpoint='tweets_secondary')
@login_required
def tweets():
    return render_template("twitter/tweets.html")

@twitter_blueprint.route("/twitter-users", methods=['GET', 'POST'])
@login_required
def twitter_users():
    if request.method == 'GET':
        return render_template("twitter/twitter-users.html")
    elif request.method == 'POST':
        try:
            tweet_user_doc = TweetUser.objects()
            twitter_users_instance = TwitterUsersUtils()
            return twitter_users_instance.get(tweet_user_doc)
        except Exception as e:
            print(e)
            return {
                'error': "Please contact to technical team or try again after a while."
            }, 500