from prometheus_client import Metric
from application import app  # Import the Flask app
from prometheus_flask_exporter import PrometheusMetrics

from routes.api.oem_routes import oem_bp
from routes.api.variant_routes import variant_bp
from routes.api.car_routes import car_bp
from routes.api.model_routes import model_bp
from routes.api.rto_routes import rto_bp


app.register_blueprint(oem_bp)
app.register_blueprint(model_bp)
app.register_blueprint(variant_bp)
app.register_blueprint(car_bp)
app.register_blueprint(rto_bp)

metrics = PrometheusMetrics(app , group_by='endpoint')

# cnt_salam_requests = metrics.counter('cnt_salam_requests', 'Number of requests to /api/salam')

# @metrics.counter('cnt_salam_requests', 'Number of requests to /api/salam')
@app.route('/api/salam')
def hello():
    return {"message": "Salam, Flask!"}


if __name__ == '__main__':
    app.run(debug=True)