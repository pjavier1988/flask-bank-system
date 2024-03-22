import os
from dotenv import load_dotenv

load_dotenv()
database_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
secret_key = os.getenv("SECRET_KEY")
jwt_secret_key = os.getenv("SECRET_KEY")

class Config:
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secret_key
    JWT_SECRET_KEY = jwt_secret_key
