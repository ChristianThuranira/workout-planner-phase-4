from flask import Blueprint, jsonify, request
from models import User, Exercise, Day, WorkoutPlan, Log
from extensions import db
from datetime import datetime

# Create a Blueprint for API routes
bp = Blueprint('main', __name__)

# Home route
@bp.route('/')
def home():
    return jsonify({"message": "Welcome to the Fitness App API"}), 200

# ------------------ User Routes ------------------
@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id, 
        'username': user.username, 
        'email': user.email
    } for user in users])

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201

# ------------------ Exercise Routes ------------------
@bp.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([{
        'id': exercise.id, 
        'name': exercise.name
    } for exercise in exercises])

@bp.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Exercise name is required"}), 400

    new_exercise = Exercise(name=data['name'])
    db.session.add(new_exercise)
    db.session.commit()
    
    return jsonify({'id': new_exercise.id, 'name': new_exercise.name}), 201

# ------------------ Day Routes ------------------
@bp.route('/days', methods=['GET'])
def get_days():
    days = Day.query.all()
    return jsonify([{
        'id': day.id, 
        'name': day.name
    } for day in days])

@bp.route('/days', methods=['POST'])
def create_day():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Day name is required"}), 400

    new_day = Day(name=data['name'])
    db.session.add(new_day)
    db.session.commit()
    
    return jsonify({'id': new_day.id, 'name': new_day.name}), 201

# ------------------ Workout Plan Routes ------------------
@bp.route('/workout-plans', methods=['GET'])
def get_workout_plans():
    workout_plans = WorkoutPlan.query.all()
    return jsonify([{
        'id': plan.id,
        'title': plan.title,
        'description': plan.description,
        'difficulty_level': plan.difficulty_level,
        'time': plan.time.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string
        'duration_minutes': plan.duration_minutes,
        'calories_burned': plan.calories_burned,
        'exercise_id': plan.exercise_id,
        'user_id': plan.user_id,
        'day_id': plan.day_id
    } for plan in workout_plans])

@bp.route('/workout-plans', methods=['POST'])
def create_workout_plan():
    data = request.get_json()
    required_fields = ["title", "description", "difficulty_level", "time", "duration_minutes", "calories_burned", "exercise_id", "user_id", "day_id"]
    if not all(k in data for k in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        parsed_time = datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400

    new_plan = WorkoutPlan(
        title=data['title'],
        description=data['description'],
        difficulty_level=data['difficulty_level'],
        time=parsed_time,
        duration_minutes=data['duration_minutes'],
        calories_burned=data['calories_burned'],
        exercise_id=data['exercise_id'],
        user_id=data['user_id'],
        day_id=data['day_id']
    )
    db.session.add(new_plan)
    db.session.commit()
    
    return jsonify({'id': new_plan.id, 'title': new_plan.title}), 201

# ------------------ Log Routes ------------------
@bp.route('/logs', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    return jsonify([{
        'id': log.id,
        'completed_date': log.completed_date.strftime('%Y-%m-%d'),
        'rating': log.rating,
        'notes': log.notes,
        'workout_id': log.workout_id
    } for log in logs])

@bp.route('/logs', methods=['POST'])
def create_log():
    data = request.get_json()
    if not all(k in data for k in ("completed_date", "rating", "notes", "workout_id")):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        completed_date = datetime.strptime(data['completed_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    new_log = Log(
        completed_date=completed_date,
        rating=data['rating'],
        notes=data['notes'],
        workout_id=data['workout_id']
    )
    db.session.add(new_log)
    db.session.commit()
    
    return jsonify({'id': new_log.id, 'completed_date': new_log.completed_date.strftime('%Y-%m-%d')}), 201
