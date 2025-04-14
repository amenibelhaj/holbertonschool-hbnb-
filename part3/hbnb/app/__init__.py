from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import DevelopmentConfig  # Import actual class, not string

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register namespaces
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Optional: create tables (mostly for development)
    with app.app_context():
        db.create_all()

    return app
