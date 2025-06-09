from models.Variant import CarModelVariant  # Import the OEM model
from flask import Blueprint

variant_bp = Blueprint('variant_routes', __name__)

@variant_bp.route('/api/variants')
def get_carModelVariants():
    variants = CarModelVariant.query.all()
    return  [variant.to_dict() for variant in variants]

# Example of a CarModelVariant record in the database
# id	variant	                    car_model_id
# 213	110PS Diesel RxZ	        57
# 451	85PS Diesel RxL	            57
# 485	85PS Diesel RxE	            57
# 652	85PS Diesel RxL Plus	    57
# 681	85PS Diesel RxL Optional	57
# 771	110PS Diesel RxL	        57
# 843	110PS Diesel RxZ Plus	    57
# 999	Petrol RxL	                57
# 1006	RXL AWD	                    57
# 1295	85PS Diesel RxZ	            57
# 1348	110PS Diesel RxZ AWD	    57
