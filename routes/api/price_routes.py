from flask import Blueprint
from models.OEM import OEM  # Import the OEM model
import pickle
from config import PRICE_PREDICTOR_MODEL_PATH

price_bp = Blueprint('price_routes', __name__)
model_load=pickle.load(open(file=PRICE_PREDICTOR_MODEL_PATH,mode='rb'))

# @metrics.counter('cnt_oems', 'Number of requests to /api/oems')
@price_bp.route('/api/price/<int:id>')
def get_oems(id):
    prices = OEM.query.all()
    return [price.to_dict() for price in prices]