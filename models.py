from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    #first_name = db.StringProperty(required = True)
    #last_name = db.StringProperty(required = True)
    #phone_num = db.PhoneNumberProperty(required = True)
    email = db.EmailProperty()
    #address = db.PostalAddressProperty()

class Course(db.Model):
    name = db.StringProperty(required = True)
    description = db.TextProperty(required = True)
    instructor = db.StringProperty(required = True)

class MyCourse(db.Model):
    name = db.StringProperty(required = True)
    description = db.TextProperty(required = True)
    instructor = db.StringProperty(required = True)
    user = db.ReferenceProperty(User, required = True)
