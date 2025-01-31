from flask import Blueprint, jsonify, request
from models import User, Exercise, Day, WorkoutPlan, Log
from extensions import db
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return jsonify({"message": "Welcome to the Fitness App API"}), 200

# ------------------ User Routes ------------------
@bp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([{ 'id': user.id, 'username': user.username, 'email': user.email } for user in users])
    
    data = request.get_json()
    if not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201

@bp.route('/users/<int:id>', methods=['PATCH', 'DELETE'])
def modify_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# ------------------ Exercise Routes ------------------
@bp.route('/exercises', methods=['GET', 'POST'])
def exercises():
    if request.method == 'GET':
        exercises = Exercise.query.all()
        return jsonify([{ 'id': exercise.id, 'name': exercise.name } for exercise in exercises])
    
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Exercise name is required"}), 400
    
    new_exercise = Exercise(name=data['name'])
    db.session.add(new_exercise)
    db.session.commit()
    return jsonify({'id': new_exercise.id, 'name': new_exercise.name}), 201

@bp.route('/exercises/<int:id>', methods=['PATCH', 'DELETE'])
def modify_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    if request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(exercise, key, value)
        db.session.commit()
        return jsonify({'message': 'Exercise updated successfully'})
    
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted successfully'})

# ------------------ Day Routes ------------------
@bp.route('/days', methods=['GET', 'POST'])
def days():
    if request.method == 'GET':
        days = Day.query.all()
        return jsonify([{ 'id': day.id, 'name': day.name } for day in days])
    
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Day name is required"}), 400
    
    new_day = Day(name=data['name'])
    db.session.add(new_day)
    db.session.commit()
    return jsonify({'id': new_day.id, 'name': new_day.name}), 201

@bp.route('/days/<int:id>', methods=['PATCH', 'DELETE'])
def modify_day(id):
    day = Day.query.get_or_404(id)
    if request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(day, key, value)
        db.session.commit()
        return jsonify({'message': 'Day updated successfully'})
    
    db.session.delete(day)
    db.session.commit()
    return jsonify({'message': 'Day deleted successfully'})

# ------------------ Workout Plan Routes ------------------
@bp.route('/workout-plans', methods=['GET', 'POST'])
def workout_plans():
    if request.method == 'GET':
        workout_plans = WorkoutPlan.query.all()
        return jsonify([{ 'id': plan.id, 'title': plan.title } for plan in workout_plans])
    
    data = request.get_json()
    required_fields = ["title", "description", "difficulty_level", "time", "duration_minutes", "calories_burned", "exercise_id", "user_id", "day_id"]
    if not all(k in data for k in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_plan = WorkoutPlan(**data)
    db.session.add(new_plan)
    db.session.commit()
    return jsonify({'id': new_plan.id, 'title': new_plan.title}), 201

@bp.route('/workout-plans/<int:id>', methods=['PATCH', 'DELETE'])
def modify_workout_plan(id):
    plan = WorkoutPlan.query.get_or_404(id)
    if request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(plan, key, value)
        db.session.commit()
        return jsonify({'message': 'Workout plan updated successfully'})
    
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'message': 'Workout plan deleted successfully'})

# ------------------ Log Routes ------------------
@bp.route('/logs', methods=['GET', 'POST'])
def logs():
    if request.method == 'GET':
        logs = Log.query.all()
        return jsonify([{ 'id': log.id, 'completed_date': log.completed_date.strftime('%Y-%m-%d') } for log in logs])
    
    data = request.get_json()
    new_log = Log(**data)
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'id': new_log.id, 'completed_date': new_log.completed_date.strftime('%Y-%m-%d')}), 201

@bp.route('/logs/<int:id>', methods=['PATCH', 'DELETE'])
def modify_log(id):
    log = Log.query.get_or_404(id)
    if request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(log, key, value)
        db.session.commit()
        return jsonify({'message': 'Log updated successfully'})
    
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Log deleted successfully'})
