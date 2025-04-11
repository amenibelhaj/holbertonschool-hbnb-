# app/models/user.py

from app import db
from flask_bcrypt import Bcrypt
import re
import uuid
bcrypt = Bcrypt()  # Initialize Bcrypt

class User(db.Model):
    """Represents a User in the HBNB app"""
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  # Store hashed password
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)  # Set password securely
        self.is_admin = is_admin
        self.validate_user()
    def set_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    def validate_user(self):
        """Validate user information"""
        if not self.first_name:
            raise ValueError("First name is required")
        if not self.last_name:
            raise ValueError("Last name is required")
        if not self.email:
            raise ValueError("Email is required")
        if not self.password:
            raise ValueError("Password is required")
        # Email validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")
