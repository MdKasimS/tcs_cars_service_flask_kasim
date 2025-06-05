from models.Database import db

class CarModelVariant(db.Model):
    __tablename__ = 'rest_carmodelvariant'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    variant = db.Column(db.String(100))
    car_model_id = db.Column(db.Integer)

    def to_dict(self):
        return {"id": self.id, "variant": self.variant, "car_model_id": self.car_model_id}
    
