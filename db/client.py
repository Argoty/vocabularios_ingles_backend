from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
# Conexión local a la base de datos
# db_client = MongoClient().local


# Conexión a la base de datos en la nube
db_client = MongoClient(os.environ.get("MONGODB_URL")).test