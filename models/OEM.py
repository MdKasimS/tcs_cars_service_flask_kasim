from models.Database import db
class OEM(db.Model):
    __tablename__ = 'rest_oem'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}