from models.Car import Car  # Import the OEM model
from flask import Blueprint

car_bp = Blueprint('car_routes', __name__)

@car_bp.route('/api/cars')
def get_cars():
    cars = Car.query.all()
    return  [car.to_dict() for car in cars]