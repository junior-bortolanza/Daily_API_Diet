from datetime import datetime
from flask import Blueprint, request, jsonify, Flask
from flask_login import current_user, login_required
from database import db
from models.meal import Meal
from models.user import User

app = Flask(__name__)
meals_bp = Blueprint('meals_route', __name__)



@meals_bp.route('/meal', methods=['POST'])
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

@meals_bp.route('/<int:id>', methods=['GET'])
def get_meal(id: int) -> int:
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

@meals_bp.route('/meals/<int:id>', methods=["GET"])
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


@meals_bp.route('/<int:id>', methods=['PUT'])
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
