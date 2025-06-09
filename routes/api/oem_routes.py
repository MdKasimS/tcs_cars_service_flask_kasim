from flask import Blueprint
from models.OEM import OEM  # Import the OEM model

oem_bp = Blueprint('oem_routes', __name__)

# @metrics.counter('cnt_oems', 'Number of requests to /api/oems')
@oem_bp.route('/api/oems')
def get_oems():
    oems = OEM.query.all()
    return [oem.to_dict() for oem in oems]

@oem_bp.route('/api/oems/<int:oem_id>')
def get_oem_by_id(oem_id):
    oem = OEM.query.get(oem_id)  # Fetch the OEM by ID
    if oem:
        return oem.to_dict()  # Convert to dictionary and return
    return {"error": "OEM not found"}, 404  # Return error if ID does not exist

# Example of an OEM record in the database    
# id	name
# 19	Mercedes-Benz


