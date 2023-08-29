from app import db
from datetime import datetime

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='user')
    expiration_time = db.Column(db.DateTime)
    date = db.Column(db.DateTime, default = datetime.now())

    forms = db.relationship("Forms", backref="user")

    def __repr__(self):
        return f'User: \n{self.id} \n{self.email} \n{self.username}'

class Forms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_title = db.Column(db.String(500), nullable=False)
    form_data = db.Column(db.String(), nullable=False)
    form_date = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f'Forms: \n{self.id} \n{self.form_data}'
