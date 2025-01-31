from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db, ma
from routes import bp as main_bp
from models import User, Exercise, Day, WorkoutPlan, Log
from datetime import datetime, date

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'  # Required for session management

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Enable CORS to allow requests from frontend (localhost:3000)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# Register the blueprint
app.register_blueprint(main_bp)

# ------------------ SESSION MANAGEMENT ------------------
@app.before_request
def ensure_session():
    if 'user_id' not in session:
        session['user_id'] = None

# ------------------ ERROR HANDLING ------------------
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

# ------------------ DATABASE SEEDING ------------------
with app.app_context():
    db.create_all()

    if not User.query.first():
        print("Seeding initial data...")
        user1 = User(username='john_doe', email='john@example.com', password='password123')
        user2 = User(username='jane_doe', email='jane@example.com', password='password123')
        db.session.add_all([user1, user2])
        db.session.commit()

        exercise1 = Exercise(name='Push-ups')
        exercise2 = Exercise(name='Squats')
        db.session.add_all([exercise1, exercise2])
        db.session.commit()

        day1 = Day(name='Monday')
        day2 = Day(name='Wednesday')
        db.session.add_all([day1, day2])
        db.session.commit()

        workout1 = WorkoutPlan(
            title='Morning Workout',
            description='A quick morning routine',
            difficulty_level='Beginner',
            time=datetime.now(),
            duration_minutes=30,
            calories_burned=200,
            exercise_id=exercise1.id,
            user_id=user1.id,
            day_id=day1.id
        )
        db.session.add(workout1)
        db.session.commit()

        log1 = Log(
            completed_date=date.today(),
            rating=5,
            notes='Great workout!',
            workout_id=workout1.id
        )
        db.session.add(log1)
        db.session.commit()

        print("Database seeding completed successfully!")
    else:
        print("Database already contains data, skipping seeding.")

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
