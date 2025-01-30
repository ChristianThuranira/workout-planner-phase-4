from flask import Blueprint, jsonify, request
from models import User, Exercise, Day, WorkoutPlan, Log
from extensions import db

# Create a Blueprint for your routes
bp = Blueprint('main', __name__)

# Home route
@bp.route('/')
def home():
    return "Welcome to the Fitness App API"

# User routes
@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201

# Exercise routes
@bp.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([{'id': exercise.id, 'name': exercise.name} for exercise in exercises])

@bp.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    new_exercise = Exercise(name=data['name'])
    db.session.add(new_exercise)
    db.session.commit()
    return jsonify({'id': new_exercise.id, 'name': new_exercise.name}), 201

# Day routes
@bp.route('/days', methods=['GET'])
def get_days():
    days = Day.query.all()
    return jsonify([{'id': day.id, 'name': day.name} for day in days])

@bp.route('/days', methods=['POST'])
def create_day():
    data = request.get_json()
    new_day = Day(name=data['name'])
    db.session.add(new_day)
    db.session.commit()
    return jsonify({'id': new_day.id, 'name': new_day.name}), 201

# Workout Plan routes
@bp.route('/workout-plans', methods=['GET'])
def get_workout_plans():
    workout_plans = WorkoutPlan.query.all()
    return jsonify([{
        'id': plan.id,
        'title': plan.title,
        'description': plan.description,
        'difficulty_level': plan.difficulty_level,
        'time': plan.time,
        'duration_minutes': plan.duration_minutes,
        'calories_burned': plan.calories_burned,
        'exercise_id': plan.exercise_id,
        'user_id': plan.user_id,
        'day_id': plan.day_id
    } for plan in workout_plans])

@bp.route('/workout-plans', methods=['POST'])
def create_workout_plan():
    data = request.get_json()
    new_plan = WorkoutPlan(
        title=data['title'],
        description=data['description'],
        difficulty_level=data['difficulty_level'],
        time=data['time'],
        duration_minutes=data['duration_minutes'],
        calories_burned=data['calories_burned'],
        exercise_id=data['exercise_id'],
        user_id=data['user_id'],
        day_id=data['day_id']
    )
    db.session.add(new_plan)
    db.session.commit()
    return jsonify({'id': new_plan.id, 'title': new_plan.title}), 201

# Log routes
@bp.route('/logs', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    return jsonify([{
        'id': log.id,
        'completed_date': log.completed_date,
        'rating': log.rating,
        'notes': log.notes,
        'workout_id': log.workout_id
    } for log in logs])

@bp.route('/logs', methods=['POST'])
def create_log():
    data = request.get_json()
    new_log = Log(
        completed_date=data['completed_date'],
        rating=data['rating'],
        notes=data['notes'],
        workout_id=data['workout_id']
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'id': new_log.id, 'completed_date': new_log.completed_date}), 201