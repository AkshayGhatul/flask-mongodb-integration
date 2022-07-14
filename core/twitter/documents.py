from core import db

class TweetUser(db.DynamicDocument):
    user_id = db.DynamicField(unique=True)

class Tweet(db.DynamicDocument):
    user = db.ReferenceField(TweetUser, reverse_delete_rule=db.CASCADE)
