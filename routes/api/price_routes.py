from flask import Blueprint, json
from sklearn.preprocessing import PolynomialFeatures
from models.Car import Car  
import pickle
from config import Config 
import pandas as pd


price_bp = Blueprint('price_routes', __name__)
model_load = pickle.load(open(file=Config.PRICE_PREDICTOR_MODEL_PATH,mode='rb'))

class CustomEncoder():
    fuels = {
        'CNG': 0,
        'Diesel': 1,
        'Electric': 2,        
        'LPG': 3,
        'Petrol': 4,
    }
    
    ownerType ={
        'First Owner': 0,
        'Fourth & Above Owner': 1,
        'Second Owner': 2,
        'Test Drive Car': 3,
        'Third Owner': 4
    } 

    transmissions = {
        "Automatic": 0,  
        "Manual": 1,     
    }   
    
    sellers = {   
        'Dealer': 0,
        'Individual': 1,
        'Trustmark Dealer': 2
    }    
    
    km_ranges = {
        "high": 0,
        "low": 1,
        "medium": 2,
    } 

    year_ranges={
        'Best': 0,
        'Buy': 1,
        'Junk': 2,
        'Scrap': 3,
    }

    ex_ranges = {
        'Affordable': 0,
        'family': 1,
        'Luxury': 2,
        'Premium': 3
    }
 
    maxValues = {
        'year': 2020.0,
        'km_driven':806599.0,
        'fuel':4.0,
        'seller_type':2.0,
        'transmission':1.0,
        'owner':4.0,
        'rating':15.0,
        'company_name':28.0,
        'km_range':2.0,
        'year_range':3.0,
        'ex_range':3.0,
    }

    modelSpecificColumns = [
        'year',
        'km_driven',
        'fuel',
        'seller_type',
        'transmission',
        'owner',
        'rating',
        'company_name',
        'km_range',
        'year_range',
        'ex_range'
    ]
# @metrics.counter('cnt_oems', 'Number of requests to /api/oems')
@price_bp.route('/api/price/<int:id>', methods=['GET'])
def get_pricePrediction(id):

    carById = Car.query.get(id)
    # carById.to_dict() - Car object must be serialized to a dictionary
    carById = pd.DataFrame([carById.to_dict()])  # Convert to DataFrame for processing

    km_ranges=['low','medium','high']
    limits=[0,35000,100000,2000000]
    carById['km_range']=pd.cut(carById['km_driven'],bins=limits,labels=km_ranges)
    
    year_ranges=['Junk','Scrap','Buy','Best']
    limits=[1991,2005,2010,2015,2020]
    carById['year_range']=pd.cut(carById['year'],bins=limits,labels=year_ranges)

    ex_range=['Affordable','family','Luxury','Premium']
    limits=[0,500000,1000000,1500000,20000000]
    carById['ex_range']=pd.cut(carById['car_showroom_price'],bins=limits,labels=ex_range)

    
    carById['fuel']= CustomEncoder.fuels[carById['fuel'].values[0]]  # Convert fuel type to numerical value
    carById['owner']= CustomEncoder.ownerType[carById['owner'].values[0]] # Convert owner type to numerical value
    carById['transmission']= CustomEncoder.transmissions[carById['transmission'].values[0]]  # Convert transmission type to numerical value
    carById['seller_type']= CustomEncoder.sellers[carById['seller_type'].values[0]]  # Convert seller type to numerical value
    carById['company_name']= carById['name_id'].values[0]  # Assuming name_id is the company ID
    carById['km_range']= CustomEncoder.km_ranges[carById['km_range'].values[0]]  # Convert km_range to numerical value
    carById['year_range']= CustomEncoder.year_ranges[carById['year_range'].values[0]]  # Convert year_range to numerical value
    carById['ex_range']= CustomEncoder.ex_ranges[carById['ex_range'].values[0]]  # Convert ex_range to numerical value
    
    

    # Ensure only the model-specific columns are retained
    modelSpecificCarData = carById[CustomEncoder.modelSpecificColumns].copy()

    for colName in CustomEncoder.maxValues:
        modelSpecificCarData[colName] = modelSpecificCarData[colName].astype('float64')
        modelSpecificCarData[colName].values[0] = modelSpecificCarData[colName].values[0] / CustomEncoder.maxValues[colName]
        
    round(modelSpecificCarData.describe(),2)

    poly_reg = PolynomialFeatures(degree=2)
    modelSpecificCarData = poly_reg.fit_transform(modelSpecificCarData)

    predictedSellingCarPriceById =  model_load.predict(modelSpecificCarData)[0]
    
    # ------------------ Output -------------------
    # Error:-> return jsonify({"selling_price":carById.to_dict()})
    # Flask's jsonify function expects a dictionary or list, not a DataFrame
    # Convert DataFrame to dictionary and then to JSON
    # It happened due to presence of numpy.int64 values in the DataFrame
    # which are not JSON serializable by default.

    # Same issue of numpy.int64 values in the DataFrame
    # return jsonify({
    #     # "selling_price": model_load.predict(carById)[0],
    #     "year": carById['year'].values[0],
    #     "km_driven": carById['km_driven'].values[0],
    #     "fuel": carById['fuel'].values[0],
    #     "seller_type": carById['seller_type'].values[0],
    #     "transmission": carById['transmission'].values[0],
    #     "owner": carById['owner'].values[0],
    #     "rating": carById['rating'].values[0],
    #     "company_name": carById['company_name'].values[0],
    #     "km_range": carById['km_range'].values[0],
    #     "year_range": carById['year_range'].values[0],
    #     "ex_range": carById['ex_range'].values[0]
    # })     

    # This does not work as well
    # due to maximu recursion level reached
    # return carById.to_json(orient="records")

    # Worked only to Convert DataFrame to dictionary without index with orient="records"
    # return json.dumps(carById.to_dict(orient="records")), 200, {'Content-Type': 'application/json'}

    # Keep this for easier data testing
    # return json.dumps({"Actual Data": carById.to_dict(orient="records"),
    #                     "Transformed Data": modelSpecificCarData.tolist(),
    #                    "Predicted Selling Price": predictedSellingCarPriceById}), 200 , {'Content-Type': 'application/json'}   
                       
                       
    return json.dumps({"selling_price": predictedSellingCarPriceById}), 200, {'Content-Type': 'application/json'}   



# ----Model Specific Data Formatting----------
    
    # "id": 11,

    # "car_showroom_price": 737176,
    # "ex_range": "family",
    
    # "name_id": 10,
    # "company_name": "Renault",
    
    # "year": 2014,
    # "year_range": "Buy"

    # "fuel": "Diesel",
    
    # "km_driven": 66569,
    # "km_range": "medium",
    
    # "owner": "First Owner",
    
    # "rating": 8,
    
    # "seller_type": "Dealer",
    
    # "transmission": "Manual",