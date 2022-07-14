from core import db

class Movie(db.Document):
    title = db.StringField(required=True)
    year = db.IntField()
    rated = db.StringField()
    director = db.ReferenceField("User", required=True)
    cast = db.ReferenceField("User", required=True)
    poster = db.FileField()