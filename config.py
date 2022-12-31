import os 
#para hacer uso de la linea 4 se debe de instalar la siguiente libreria
#pip install python-dotenv
from dotenv import load_dotenv
#accediendo al archivo .env mediante dotenv
dotenv_path=os.path.join(os.path.dirname(__file__),'.env')
load_dotenv(dotenv_path)

FLASK_DEBUG = os.environ.get("FLASK_DEBUG",False)
TESTING = os.environ.get("TESTING",False)
SECRET_KEY = os.environ.get("SECRET_KEY",False)

SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO",False)
SQLALCHEMY_TRACK_MODIFICATION = os.environ.get("SQLALCHEMY_TRACK_MODIFICATION",False)
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI","")

JSON_SORT_KEYS=False


