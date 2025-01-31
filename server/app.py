from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from routes import bp as main_bp
from models import User, Exercise, Day, WorkoutPlan, Log
from datetime import datetime, date

# Initialize Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Register the blueprint
app.register_blueprint(main_bp)

# Create the database and seed initial data
with app.app_context():
    # Create the database and tables if they do not exist
    db.create_all()
    
    # Check if the database already has data to avoid duplicates
    if not User.query.first():
        print("Seeding initial data...")

        # Add Users
        user1 = User(username='john_doe', email='john@example.com', password='password123')
        user2 = User(username='jane_doe', email='jane@example.com', password='password123')
        db.session.add_all([user1, user2])
        db.session.commit()  # Commit so we can use their IDs

        # Add Exercises
        exercise1 = Exercise(name='Push-ups')
        exercise2 = Exercise(name='Squats')
        db.session.add_all([exercise1, exercise2])
        db.session.commit()
        
        # Add Days
        day1 = Day(name='Monday')
        day2 = Day(name='Wednesday')
        db.session.add_all([day1, day2])
        db.session.commit()

        # Add Workout Plans
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

        # Add Logs
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
    app.run(debug=True)
