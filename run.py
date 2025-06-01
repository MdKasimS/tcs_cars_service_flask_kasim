from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by='endpoint')

# PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/TheCarShopDb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# @metrics.counter('cnt_users', 'Number of requests to /api/salam')
@app.route('/api/salam')
def hello():
    return {"message": "Salam, Flask!"}


class OEM(db.Model):
    __tablename__ = 'rest_oem'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)


    def to_dict(self):
        return {"id": self.id, "name": self.name}

class CarModel(db.Model):
    __tablename__ = 'rest_carmodel'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    oem_id = db.Column(db.Integer)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "oem_id": self.oem_id}

class CarModelVariant(db.Model):
    __tablename__ = 'rest_carmodelvariant'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    variant = db.Column(db.String(100))
    car_model_id = db.Column(db.Integer)

    def to_dict(self):
        return {"id": self.id, "variant": self.variant, "car_model_id": self.car_model_id}

class Car(db.Model):
    __tablename__ = 'rest_car'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    car_showroom_price = db.Column(db.Integer)
    year = db.Column(db.Integer)
    km_driven = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    car_model_id = db.Column(db.Integer)
    car_variant_id = db.Column(db.Integer)
    name_id = db.Column(db.Integer)
    fuel = db.Column(db.String(100))
    seller_type = db.Column(db.String(100))
    transmission = db.Column(db.String(100))
    owner = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "car_showroom_price": self.car_showroom_price,
            "year": self.year,
            "km_driven": self.km_driven,
            "rating": self.rating,
            "car_model_id": self.car_model_id,
            "car_variant_id": self.car_variant_id,
            "name_id": self.name_id,
            "fuel": self.fuel,
            "seller_type": self.seller_type,
            "transmission": self.transmission,
            "owner": self.owner
        }

class RtoNumber(db.Model):
    __tablename__ = 'rest_rto'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer)
    rto_number = db.Column(db.String(100))

    def to_dict(self):
        return {"id": self.id, "car_id": self.car_id, "rto_number": self.rto_number}

# @metrics.counter('cnt_oems', 'Number of requests to /api/oems')
@app.route('/api/oems')
def get_oems():
    oems = OEM.query.all()
    return [oem.to_dict() for oem in oems]

@app.route('/api/oems/<int:oem_id>')
def get_oem_by_id(oem_id):
    oem = OEM.query.get(oem_id)  # Fetch the OEM by ID
    if oem:
        return oem.to_dict()  # Convert to dictionary and return
    return {"error": "OEM not found"}, 404  # Return error if ID does not exist

@app.route('/api/models')
def get_carModels():
    models = CarModel.query.all()
    return  [model.to_dict() for model in models]

@app.route('/api/variants')
def get_carModelVariants():
    variants = CarModelVariant.query.all()
    return  [variant.to_dict() for variant in variants]

@app.route('/api/cars')
def get_cars():
    cars = Car.query.all()
    return  [car.to_dict() for car in cars]

@app.route('/api/rtos')
def get_rtoNumbers():
    rtos = RtoNumber.query.all()
    return  [rto.to_dict() for rto in rtos]




if __name__ == '__main__':
    app.run(debug=True)