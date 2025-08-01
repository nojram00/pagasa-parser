from mongoengine import *
import dotenv
import os

dotenv.load_dotenv()

def setup_db():
    connect(host=os.getenv('MONGO_DB_URI'), alias="default", db="pagasa-weather-forecast")
