from models.Variant import CarModelVariant  # Import the OEM model
from flask import Blueprint

variant_bp = Blueprint('variant_routes', __name__)

@variant_bp.route('/api/variants')
def get_carModelVariants():
    variants = CarModelVariant.query.all()
    return  [variant.to_dict() for variant in variants]