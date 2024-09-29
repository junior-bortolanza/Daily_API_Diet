from flask import Flask
from database import db
from models.meal import Meal

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello, world"

if __name__ == '__main__':
    app.run(debug=True)