from flask import Flask, request
from database import db
from models.meal import Meal

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

# Create CRUD: Create, Read, Update and DELETE

@app.route('/', methods=['POST'])
def create_meal():
    data = request.json
    name = data.json.get('name')
    description = data.json.get('description')
    date_on_meal = data.json.get('date_time_meal')
    meal_on_diet = data.json.get('meal_on_diet')

    
    



if __name__ == '__main__':
    app.run(debug=True)