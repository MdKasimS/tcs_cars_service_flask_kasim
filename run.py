from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by='endpoint')

# PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/TheCarShopDb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@metrics.counter('cnt_users', 'Number of requests to /api/salam')
@app.route('/api/salam')
def hello():
    return {"message": "Salam, Flask!"}


class User(db.Model):
    __tablename__ = 'rest_oem'  # Match existing table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@metrics.counter('cnt_oems', 'Number of requests to /api/oems')
@app.route('/api/oems')
def get_users():
    oems = User.query.all()
    return {"users": [{"id": oem.id, "name": oem.name,} for oem in oems]}

if __name__ == '__main__':
    app.run(debug=True)