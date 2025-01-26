# Este fichero es el encargado de gestionar la conección con la base de datos de MongoDB.

### MongoDB client ###

# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# Módulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost



from pymongo import MongoClient

# Base de datos Local
db_client = MongoClient().local

# Base de datos Remota  
#db_client = MongoClient(
#   'mongodb+srv://test:test@cluster0.q9a4d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0').test