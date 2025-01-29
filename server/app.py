from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, User, Exercise, Day, WorkoutPlan, Log

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Fitness App API"})

if __name__ == '__main__':
    app.run(debug=True)