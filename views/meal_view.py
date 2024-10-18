from datetime import datetime
from flask import Blueprint, request, jsonify, Flask
from database import db
from models.meal import Meal


app = Flask(__name__)
meals_bp = Blueprint('meals_route', __name__)


@meals_bp.route('/meal', methods=['POST'])
def create_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    meal_time = data.get("meal_time")
    hour_meal = data.get("hour_meal")
    on_diet = data.get("on_diet")

    if name and description and on_diet:
        meal = Meal(
                name=name,
                description=description,
                meal_time=meal_time,
                hour_meal=hour_meal,
                on_diet=on_diet,
            )
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message":"Meal has been created"})
    return jsonify({"message": "Inválid description"}), 400
            

@meals_bp.route('/<int:id>', methods=['GET'])
def get_meal(id: int) -> int:
    meal = Meal.query.get(id)

    if meal:
        return {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "meal_time": meal.meal_time,
            "hour_meal": meal.hour_meal,
            "on_diet": meal.on_diet
        }
    return jsonify({"message": "Meal no found"}), 404

@meals_bp.route('/meals', methods=["GET"])
def get_meals() -> str:
    meals = Meal.query.all()

    meal_list = []
    for meal in meals:
                meal_data = {
                    "id":meal.id,
                    "name": meal.name,
                    "description": meal.description,
                    "meal_time": meal.meal_time,
                    "hour_meal": meal.hour_meal,
                    "on_diet": meal.on_diet
                }
    meal_list.append(meal_data)
    return jsonify(meal_list)
    


