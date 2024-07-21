from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()  # Define db

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.String, nullable=False)
    cin = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    service = db.Column(db.String, nullable=False)
    site = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return str(self.id)

class Quiz(db.Model):
    __tablename__ = 'Quizzes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    questions = db.relationship('Question', back_populates='quiz')

class Question(db.Model):
    __tablename__ = 'Questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quizzes.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    quiz = db.relationship('Quiz', back_populates='questions')
    options = db.relationship('Option', back_populates='question')

class Option(db.Model):
    __tablename__ = 'Options'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('Questions.id'), nullable=False)
    text = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    question = db.relationship('Question', back_populates='options')

class Attempt(db.Model):
    __tablename__ = 'Attempts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quizzes.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, nullable=False)

class Answer(db.Model):
    __tablename__ = 'Answers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('Attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('Questions.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('Options.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
