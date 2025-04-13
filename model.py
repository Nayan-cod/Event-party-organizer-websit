from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10))  # customer or organizer
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    mobile = db.Column(db.String(15))  # New field
    password = db.Column(db.String(200))

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    organizer = db.relationship('User', backref='services')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    status = db.Column(db.String(20))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)