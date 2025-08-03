# Simple user routes
from flask import Blueprint, request, jsonify
from models.user import (
    create_user, get_all_users, get_user_by_id, 
    update_user, delete_user, search_users_by_name, authenticate_user
)

# Create a blueprint for user routes
user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def home():
    return jsonify({"message": "User Management System"}), 200

@user_routes.route('/users', methods=['GET'])
def get_users():
    try:
        users = get_all_users()
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": "Could not get users"}), 500

@user_routes.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = get_user_by_id(id)
        if user:
            return jsonify({"user": user}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Could not get user"}), 500

@user_routes.route('/users', methods=['POST'])
def create_new_user():
    try:
        data = request.get_json()
        if not data or not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Name, email and password are required"}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
 
        if '@' not in email:
            return jsonify({"error": "Invalid email format"}), 400
        
        success = create_user(name, email, password)
        if success:
            return jsonify({"message": "User created successfully"}), 201
        else:
            return jsonify({"error": "User already exists"}), 409
            
    except Exception as e:
        return jsonify({"error": "Could not create user"}), 500

@user_routes.route('/user/<int:id>', methods=['PUT'])
def update_existing_user(id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name', '').strip() if data.get('name') else None
        email = data.get('email', '').strip().lower() if data.get('email') else None
        
        if not name and not email:
            return jsonify({"error": "Name or email must be provided"}), 400
        
        if email and '@' not in email:
            return jsonify({"error": "Invalid email format"}), 400
        
        success = update_user(id, name, email)
        if success:
            return jsonify({"message": "User updated successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"error": "Could not update user"}), 500

@user_routes.route('/user/<int:id>', methods=['DELETE'])
def delete_existing_user(id):
    try:
        success = delete_user(id)
        if success:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"error": "Could not delete user"}), 500

@user_routes.route('/search', methods=['GET'])
def search_users():
    try:
        name = request.args.get('name', '').strip()
        
        if not name:
            return jsonify({"error": "Please provide a name to search"}), 400
        
        users = search_users_by_name(name)
        return jsonify({"users": users}), 200
        
    except Exception as e:
        return jsonify({"error": "Could not search users"}), 500

@user_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password are required"}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        user = authenticate_user(email, password)
        if user:
            return jsonify({"status": "success", "user": user}), 200
        else:
            return jsonify({"status": "failed", "error": "Invalid email or password"}), 401
            
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500
