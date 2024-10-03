from flask import Flask, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from database import db
from models.meal import Meal
from models.user import User


app = Flask(__name__)
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
    date_time_meal = data.get("date_time_meal")
    hour_meal = data.get("hour_meal")























@app('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticateded)
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
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"User has been created!"})
    return jsonify({"message": "Invalid datas"}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
def get_user(id_user):
    user = User.query.get(id_user)

    if User:
        return {"username": user.username}
    return jsonify({"message": "User not found"}), 404


@app.route('/user/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if User and data.get("password"):
        user.password = data.get("password")
        db.session.commit()

        return jsonify({"message": f"User {id_user} has been updated successful!"})
    
    return jsonify({"message": "User not found!"}), 404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if id_user == current_user.id:
        return jsonify({"message": "Delete not allow"}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":f"User {id_user} has been deleted successful!"})
    
    return jsonify({"message": "User not found!"}), 404
    






    

        
    

   

    
    



if __name__ == '__main__':
    app.run(debug=True)