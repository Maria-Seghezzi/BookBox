from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    reviews = db.relationship("Review")
    books = db.relationship("UserBooks")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    category = db.Column(db.String())
    description = db.Column(db.String())
    page_number = db.Column(db.Integer)
    language = db.Column(db.String())
    publisher = db.Column(db.String())
    isbn = db.Column(db.Integer(), unique=True)
    reviews = db.relationship("Review")

class UserBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    status = db.Column(db.String())
    date_started = db.Column(db.Date())
    date_finished = db.Column(db.Date())

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    person_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    person_username = db.Column(db.String())
    text = db.Column(db.String())
    stars = db.Column(db.Integer)
    date = db.Column(db.Date())
