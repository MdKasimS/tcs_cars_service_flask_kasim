import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/TheCarShopDb'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PRICE_PREDICTOR_MODEL_PATH = os.path.join(BASE_DIR, "resources", "aiml_models", "Most_Accurate_Reg_Model.sav")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        self.printPath()

    def printPath(self):
        print("Config Path: ", self.BASE_DIR)
        print("Price Predictor Model Path: ", self.PRICE_PREDICTOR_MODEL_PATH)
