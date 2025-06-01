from flask import Flask

app = Flask(__name__)

@app.route('/api/salam')
def hello():
    return {"message": "Salam, Flask!"}

if __name__ == '__main__':
    app.run(debug=True)