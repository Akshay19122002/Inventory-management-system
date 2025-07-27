from flask import Blueprint, request, jsonify
from ..models import User  # Use relative import '..' to go up one level to app/
from .. import db, bcrypt # Use relative import '..' to get db and bcrypt from __init__.py
from flask_jwt_extended import create_access_token
from flask_login import login_user, logout_user, login_required

# This is the correct way to define your blueprint
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    # ... your registration logic here ...
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing email or password"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered"}), 409
    
    new_user = User(email=data['email'], role=data.get('role', 'Staff'))
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth.route('/login', methods=['POST'])
def login():
    # ... your login logic here ...
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing email or password"}), 400
        
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        login_user(user) # For Flask-Login session
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=user.email, additional_claims=additional_claims
        )
        return jsonify(access_token=access_token, user={"email": user.email, "role": user.role})
    
    return jsonify({"message": "Invalid credentials"}), 401

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Successfully logged out"}), 200
