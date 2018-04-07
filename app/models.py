from app import db

class User(db.Document):
    email = db.StringField(max_length=40)
    prefs = db.ListField(db.StringField(max_length=40))

    def __unicode__(self):
        return self.email.split('@')[0]
