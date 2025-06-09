from models.Model import CarModel  # Import the OEM model
from flask import Blueprint

model_bp = Blueprint('model_routes', __name__)

@model_bp.route('/api/models')
def get_carModels():
    models = CarModel.query.all()
    return  [model.to_dict() for model in models]

# Example of a CarModel record in the database
# id	name	oem_id
# 57	Duster	10
