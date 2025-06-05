from models.RTO import RtoNumber  # Import the OEM model
from flask import Blueprint

rto_bp = Blueprint('rto_routes', __name__)

@rto_bp.route('/api/rtos')
def get_rtoNumbers():
    rtos = RtoNumber.query.all()
    return  [rto.to_dict() for rto in rtos]
