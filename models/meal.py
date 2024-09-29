from database import db

class Meal(db.Model):
    
    # id, nome, descrição, horário da refeição, refeição na dieta ou não.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True )
    description = db.Column(db.String, nullable=False)
    date_time_meal = db.Column(db.DateTime)
    meal_on_diet = db.Column(db.Boolean, default=False)
