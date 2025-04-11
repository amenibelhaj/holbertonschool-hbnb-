from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.services import facade
from app.services.facade import HBnBFacade
from app.models.user import User  # Ensure you import the User model

api = Namespace('login', description='User authentication')

# Request model for login
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.check_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        access_token = create_access_token(identity=str(user.id), additional_claims={"is_admin": user.is_admin}, expires_delta=timedelta(days=1))
        return {'access_token': access_token}, 200
    # Request model for user registration
register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Register route for user registration
@api.route('/register')
class RegisterResource(Resource):
    @api.expect(register_model)
    def post(self):
        """Register a new user"""
        data = api.payload
        # Check if the email is already in use
        existing_user = facade.get_user_by_email(data['email'])
        if existing_user:
            return {'error': 'Email already exists!'}, 400
        
        # Create a new user
        try:
            new_user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password']
            )
            facade.save_user(new_user)  # Assuming you have a method to save the user to the DB
        except ValueError as e:
            return {'error': str(e)}, 400
        
        # Generate access token after registration
        access_token = create_access_token(identity=str(new_user.id), additional_claims={"is_admin": new_user.is_admin}, expires_delta=timedelta(days=1))
        return {'access_token': access_token}, 201

facade = HBnBFacade()

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Example protected endpoint"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        return {
            'message': f'Hello, user {current_user_id}',
            'is_admin': claims.get("is_admin", False)
        }, 200

@api.route('/generate_admin_token')
class GenerateAdminToken(Resource):
    def get(self):
        ad_token = create_access_token(identity="admin", expires_delta=timedelta(days=365),
                                    additional_claims={"is_admin": True})
        return ({'admin_token': ad_token})
