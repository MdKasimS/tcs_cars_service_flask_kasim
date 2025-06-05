from models.Database import db

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