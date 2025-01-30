from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from routes import bp as main_bp  # Import the blueprint

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)