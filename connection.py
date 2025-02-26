import pymongo

connection = pymongo.MongoClient("mongodb+srv://root:Aidan9919.@cluster0.nywpd.mongodb.net/")
database = connection["agenda"]
columna = database["contactos"]

database_2 = connection['estilos']
columna_2 = database_2['estilos']

database_3 = connection['eliminados']
columna_3 = database_3['contactos_eliminados']