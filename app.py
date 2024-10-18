from views.meal_view import meals_bp, app
from database import db


app.register_blueprint(meals_bp)


app.config["SECRET_KEY"] = "my_password"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
