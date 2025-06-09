from flask import jsonify
from prometheus_client import Metric
from application import app  # Import the Flask app
from prometheus_flask_exporter import PrometheusMetrics

from models.OEM import OEM
from models.RTO import RtoNumber 
from models.Car import Car
from models.Variant import CarModelVariant
from models.Model import CarModel

from routes.api.oem_routes import oem_bp
from routes.api.variant_routes import variant_bp
from routes.api.car_routes import car_bp
from routes.api.model_routes import model_bp
from routes.api.rto_routes import rto_bp
from routes.api.price_routes import price_bp


app.register_blueprint(oem_bp)
app.register_blueprint(model_bp)
app.register_blueprint(variant_bp)
app.register_blueprint(car_bp)
app.register_blueprint(rto_bp)
app.register_blueprint(price_bp)

metrics = PrometheusMetrics(app , group_by='path')

@app.route('/api/salam', methods=['GET'])
@metrics.counter('cnt_salam_requests', 'Number of requests to /api/salam')
def hello():
    return {"message": "Salam, Flask!"}

@app.route('/api/testcars/<int:id>', methods=['GET'])
def testRoute(id):
    car = Car.query.get(id)
    oem = OEM.query.get(car.name_id)
    model = CarModel.query.get(car.car_model_id)
    variant = CarModelVariant.query.get(car.car_variant_id)
    rto = RtoNumber.query.get(car.id)
    
    return jsonify({"OEM": oem.to_dict(),
            "Model": model.to_dict(),
            "Variant": variant.to_dict(),
            "Car": car.to_dict(),
            "RTO": rto.to_dict()})

if __name__ == '__main__':
    # For prometheus please do not start Flask app in debug mode
    app.run(debug=False)

# year               2017.0
# year_range            0.0 
# transmission          1.0
# seller_type           1.0
# km_driven        120000.0
# km_range              0.0
# Rating                9.0
# owner                 0.0
# fuel                  1.0
# ex_range              3.0
# company_name         17.0

# selling_price    628000.0

# year , km_driven , fuel, seller_type, transmission , owner, Rating, selling_price, company_name, km_range, year_range , ex_range