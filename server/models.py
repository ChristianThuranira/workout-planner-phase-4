from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    workout_plans = db.relationship('WorkoutPlan', backref='user', lazy=True)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    workout_plans = db.relationship('WorkoutPlan', backref='exercise', lazy=True)

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    workout_plans = db.relationship('WorkoutPlan', backref='day', lazy=True)

class WorkoutPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty_level = db.Column(db.String(80), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    logs = db.relationship('Log', backref='workout_plan', lazy=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    completed_date = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_plan.id'), nullable=False)