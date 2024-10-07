import bcrypt
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from database import db
from models.user import User
from models.meal import Meal

user_bp = Blueprint('user_route', __name__)



@user_bp.route('/login', methods=['POST'])
def login() -> None:
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Authentication has been done successfully!"})
       
        return jsonify({"message": "Invalid credentials"}), 400
    
@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout has been success!"})


@user_bp.route('/user>', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password, role='user')
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"User has been created!"})
    
    return jsonify({"message": "Invalid datas"}), 400

@user_bp.route('/user/<int:id_user>', methods=['GET'])
def get_user(id_user: int) -> int:
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify({"message": "User not found"}), 404


@user_bp.route('/user/<int:id_user>', methods=['PUT'])
def update_user(id_user: int) -> int:
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role =="user":
        return jsonify({"message": "Operation not allowed"}), 403

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()

        return jsonify({"message": f"User {id_user} has been updated successful!"})
 
    return jsonify({"message": "User not found!"}), 404

@user_bp.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user: int) -> int:
    user = User.query.get(id_user)

    if id_user == current_user.id:
        return jsonify({"message": "Delete not allow"}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":f"User {id_user} has been deleted successful!"})
    
    return jsonify({"message": "User not found!"}), 404

@user_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_meal(id: int) -> int:
    meal = Meal.query.get(id)

    if meal:
        db.session.delete(meal)
        db.session.commit()

        return jsonify({"message": "Meal has been deleted!"})
    return jsonify({"message": "Meal not found"}), 404