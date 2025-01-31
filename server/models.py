from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from extensions import db, ma

# Association table for many-to-many relationship between Users and Exercises
user_exercise = db.Table('user_exercise',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    workout_plans = db.relationship('WorkoutPlan', backref='user', lazy=True)
    exercises = db.relationship('Exercise', secondary=user_exercise, back_populates='users')

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    workout_plans = db.relationship('WorkoutPlan', backref='exercise', lazy=True)
    users = db.relationship('User', secondary=user_exercise, back_populates='exercises')

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

# Marshmallow Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        include_relationships = True
        load_instance = True

class WorkoutPlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutPlan
        include_relationships = True
        load_instance = True

class LogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Log
        include_relationships = True
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_plan_schema = WorkoutPlanSchema()
workout_plans_schema = WorkoutPlanSchema(many=True)
log_schema = LogSchema()
logs_schema = LogSchema(many=True)
