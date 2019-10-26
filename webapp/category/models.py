from webapp.db.db import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    courses = db.relationship('Course', backref='category', lazy='dynamic')  
    def __init__(self, name):
        self.name = name  
    def __repr__(self):
        return '<Category {}>'.format(self.name)
