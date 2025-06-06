from models.Database import db

class CarModel(db.Model):
    __tablename__ = 'rest_carmodel'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    oem_id = db.Column(db.Integer)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "oem_id": self.oem_id}
