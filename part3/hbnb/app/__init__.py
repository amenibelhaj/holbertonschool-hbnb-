from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
from app.api.v1.auth import api as auth_ns
def create_app(config_class="config.DevelopmentConfig"):
    # Initialize the Flask application
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Initialize the API object after the app and extensions
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register the API namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    # Register the namespaces for the API
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Initialize models (Make sure db is already initialized before this)
    from app.models.user import User

    # Create all tables in the database when the app context is pushed
    with app.app_context():
        db.create_all()

    # Return the app object
    return app
