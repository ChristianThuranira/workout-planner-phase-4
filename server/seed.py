from app import app
from models import db, User, Exercise, Day, WorkoutPlan, Log
from datetime import datetime, date

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Add Users
    user1 = User(username='john_doe', email='john@example.com', password='password123')
    user2 = User(username='jane_doe', email='jane@example.com', password='password123')
    db.session.add(user1)
    db.session.add(user2)

    # Add Exercises
    exercise1 = Exercise(name='Push-ups')
    exercise2 = Exercise(name='Squats')
    db.session.add(exercise1)
    db.session.add(exercise2)

    # Add Days
    day1 = Day(name='Monday')
    day2 = Day(name='Wednesday')
    db.session.add(day1)
    db.session.add(day2)

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
    workout2 = WorkoutPlan(
        title='Evening Workout',
        description='An intense evening session',
        difficulty_level='Advanced',
        time=datetime.now(),
        duration_minutes=60,
        calories_burned=500,
        exercise_id=exercise2.id,
        user_id=user2.id,
        day_id=day2.id
    )
    db.session.add(workout1)
    db.session.add(workout2)

    # Add Logs
    log1 = Log(
        completed_date=date.today(),
        rating=5,
        notes='Great workout!',
        workout_id=workout1.id
    )
    log2 = Log(
        completed_date=date.today(),
        rating=4,
        notes='Feeling good!',
        workout_id=workout2.id
    )
    db.session.add(log1)
    db.session.add(log2)

    # Commit changes
    db.session.commit()

    print("Database seeded successfully!")