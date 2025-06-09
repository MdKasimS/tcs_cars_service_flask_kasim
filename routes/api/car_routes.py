from models.Car import Car  # Import the OEM model
from flask import Blueprint, jsonify, request
from models.Database import db  # Import the database instance

car_bp = Blueprint('car_routes', __name__)

@car_bp.route('/api/cars/<int:id>', methods=['GET'])
def get_car(id):
    car = Car.query.get_or_404(id) # Use get_or_404 to return 404 if car not found 
    return  jsonify(car.to_dict())

@car_bp.route('/api/cars', methods=['GET'])
def get_all_cars():
    cars = Car.query.all()
    return jsonify([car.to_dict() for car in cars])  # Return list of cars

# Create a new car record
#TODO: Please do test this POST for Cars
@car_bp.route('/api/cars', methods=['POST'])
def create_car():
    data = request.json
    new_car = Car(**data)  # Assuming car model fields match request data keys
    db.session.add(new_car)
    db.session.commit()
    return jsonify(new_car.to_dict()), 201  # Return created car data with status code

# Update an existing car record
#TODO: Please do test this for PUT for cars
@car_bp.route('/api/cars/<int:id>', methods=['PUT'])
def update_car(id):
    car = Car.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(car, key, value)  # Update fields dynamically
    db.session.commit()
    return jsonify(car.to_dict())

# Delete a car record
#TODO: Please do test this for DELETE for cars
@car_bp.route('/api/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': 'Car deleted successfully'}), 204  # No content response


# Example of a car record in the database
# id	car_showroom_price	year	km_driven	fuel	seller_type	transmission	owner	    rating	car_model_id	car_variant_id	name_id
# 15	272090	            2015	70000	    Petrol	Individual	Manual	        First Owner	9	    8	            101	            2
