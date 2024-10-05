from datetime import datetime
import bcrypt
from flask import Flask, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from database import db
from models.meal import Meal
from models.user import User


app = Flask(__name__)
app.config["SECRET_KEY"] = "my_password"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Create CRUD: Create, Read, Update and DELETE

@app.route('/meal', methods=['POST'])
def create_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    date_time = data.get("date_time")
    hour_meal = data.get("hour_meal")
    on_diet = data.get("on_diet")

    if name and date_time and hour_meal:
        date_time = datetime.strptime(date_time,"%d/%m/%Y")
        hour_meal = datetime.strptime(hour_meal, "%H:%M").strftime("%H.%M")

        if current_user.is_authenticated:
            id_user = current_user.id

            meal = Meal(
                name=name,
                description=description,
                date_time=date_time,
                hour_meal=hour_meal,
                on_diet=on_diet,
                id_user=id_user,
            )
            db.session.add(meal)
            db.session.commit()

            return jsonify({"message":"Meal has been created"})
        
        return jsonify({"message": "Invalid data"}),400

@app.route('/<int:id>', methods=['GET'])
def get_meal(id) -> int:
    meal = Meal.query.get(id)

    if meal:
        return {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "date_time": meal.date_time,
            "hour_meal": meal.hour_meal,
            "on_diet": meal.on_diet,
        }
    return jsonify({"message": "Meal no found"}), 404

@app.route('/meals/<int:id>', methods=["GET"])
def get_meals(id: int) -> int:
    user = User.query.get(id)
    meals = Meal.query.all()

    if user and current_user.is_authenticated:
        meals = Meal.query.filter_by(id_user=id).all()

        meal_list = []
        for meal in meals:
            meal_data = {
                "id":meal.id,
                "name": meal.name,
                "description": meal.description,
                "date_time": meal.date_time,
                "hour_meal": meal.hour_meal,
                "on_diet": meal.on_diet
            }
            meal_list.append(meal_data)
        return jsonify(meal_list)
    return jsonify({"message": "You aren't authorized!"}), 403


@app.route('/<int:id>', methods=['PUT'])
@login_required
def update_meals(id: int) -> int:

    data = request.json
    meal = Meal.query.get(id)

    if not current_user.is_authenticated:
        return jsonify({"message": "You can't change the meal"}), 403
    
    if meal and data.get("name"):
        meal.name = data.get("name")
        meal.description = data.get("description")
        meal.date_time = datetime.strftime(data.get("date_time"), "%d/%m/%Y")
        meal.hour_meal = datetime.strftime(data.get("hour_meal"), "%H: %M")
        meal.on_diet = data.get("on_diet")
        
        db.session.commit()
        return jsonify({"message": "Meal has been updated successfuly"})
    return jsonify({"messsage": "Meal not found!"}), 404


# Session CRUD - USERS
@app.route('/login', methods=['POST'])
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
    
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout has been success!"})


@app.route('/user>', methods=['POST'])
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

@app.route('/user/<int:id_user>', methods=['GET'])
def get_user(id_user: int) -> int:
    user = User.query.get(id_user)

    if user:
        return {"username": user.username}
    
    return jsonify({"message": "User not found"}), 404


@app.route('/user/<int:id_user>', methods=['PUT'])
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

@app.route('/user/<int:id_user>', methods=['DELETE'])
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

@app.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_meal(id: int) -> int:
    meal = Meal.query.get(id)

    if meal:
        db.session.delete(meal)
        db.session.commit()

        return jsonify({"message": "Meal has been deleted!"})
    return jsonify({"message": "Meal not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
