from pymongo import MongoClient
# Conexión local a la base de datos
# db_client = MongoClient().local


# Conexión a la base de datos en la nube
db_client = MongoClient("mongodb+srv://Javier:08102006@cluster.xzddmzj.mongodb.net/?retryWrites=true&w=majority").test