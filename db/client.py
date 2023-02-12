from pymongo import MongoClient
import os

# Conexión local a la base de datos
# db_client = MongoClient().local


# Conexión a la base de datos en la nube
db_client = MongoClient(os.environ.get("CONEXION_DB")).test