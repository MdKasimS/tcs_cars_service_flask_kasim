from models.Database import db

class RtoNumber(db.Model):
    __tablename__ = 'rest_rto'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer)
    rto_number = db.Column(db.String(100))

    def to_dict(self):
        return {"id": self.id, "car_id": self.car_id, "rto_number": self.rto_number}