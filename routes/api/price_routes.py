from flask import Blueprint, jsonify
import requests
from models.Car import Car  # Import the OEM model
import pickle
from config import Config #PRICE_PREDICTOR_MODEL_PATH
import pandas as pd
from sklearn.preprocessing import LabelEncoder    


price_bp = Blueprint('price_routes', __name__)
model_load = pickle.load(open(file=Config.PRICE_PREDICTOR_MODEL_PATH,mode='rb'))

# @metrics.counter('cnt_oems', 'Number of requests to /api/oems')
@price_bp.route('/api/price/<int:id>', methods=['GET'])
def get_pricePrediction(id):
    # predictedSellingCarPriceById = Car.query.get(id)
    carById = Car.query.get(id)
    carById = pd.DataFrame([carById.to_dict()])  # Convert to DataFrame for processing

    print(carById)

    response = requests.get("http://localhost:5000/api/oems/" + str(carById['name_id'].values[0]))
    
    if response.status_code == 200:  # Ensure request was successful
        carById['company_name'] = jsonify(response.json()) 
    else:
        return {"error": "OEM not found"}, 404
        
    km_ranges=['low','medium','high']
    limits=[0,35000,100000,2000000]
    carById['km_range']=pd.cut(carById['km_driven'],bins=limits,labels=km_ranges)
    
    year_ranges=['Junk','Scrap','Buy','Best']
    limits=[1991,2005,2010,2015,2020]
    carById['year_range']=pd.cut(carById['year'],bins=limits,labels=year_ranges)

    ex_range=['Affordable','family','Luxury','Premium']
    limits=[0,500000,1000000,1500000,20000000]
    carById['ex_range']=pd.cut(carById['car_showroom_price'],bins=limits,labels=ex_range)

    print(carById)

    # ----Lable encoding----------
    EN = LabelEncoder()
    # carById['fuel']= EN.fit_transform(carById['fuel'])
    # carById['owner']=EN.fit_transform(carById['owner'])
    # carById['transmission']=EN.fit_transform(carById['transmission'])
    # carById['name']=EN.fit_transform(carById['name'])
    # carById['seller_type']=EN.fit_transform(carById['seller_type'])
    # carById['company_name']=EN.fit_transform(carById['company_name'])
    # carById['km_range']=EN.fit_transform(carById['km_range'])
    # carById['year_range']=EN.fit_transform(carById['year_range'])
    # carById['ex_range']=EN.fit_transform(carById['ex_range'])

    return jsonify({"Selling Price": carById.to_dict()})


# year 
# km_driven 
# fuel
# seller_type
# transmission 
# owner
# Rating
# company_name
# km_range
# year_range 
# ex_range


# ----Feature Engineering-----

#Company Names
    # OEM names are directly available in api

# Kilometers
# km_ranges=['low','medium','high']
# limits=[0,35000,100000,2000000]
# data['km_range']=pd.cut(data['km_driven'],bins=limits,labels=km_ranges)

# Year
# year_ranges=['Junk','Scrap','Buy','Best']
# limits=[1991,2005,2010,2015,2020]
# data['year_range']=pd.cut(data['year'],bins=limits,labels=year_ranges)
 
# Exshowroom 
# ex_range=['Affordable','family','Luxury','Premium']
# limits=[0,500000,1000000,1500000,20000000]
# data['ex_range']=pd.cut(data['ExShowroom Price'],bins=limits,labels=ex_range)

# ----Lable encoding----------
# EN = LabelEncoder()
# data['fuel']= EN.fit_transform(data['fuel'])
# data['owner']=EN.fit_transform(data['owner'])
# data['transmission']=EN.fit_transform(data['transmission'])
# data['name']=EN.fit_transform(data['name'])
# data['seller_type']=EN.fit_transform(data['seller_type'])

# data['company_name']=EN.fit_transform(data['company_name'])
# data['km_range']=EN.fit_transform(data['km_range'])
# data['year_range']=EN.fit_transform(data['year_range'])
# data['ex_range']=EN.fit_transform(data['ex_range'])