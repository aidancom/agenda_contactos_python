import pymongo

connection = pymongo.MongoClient("mongodb+srv://root:Aidan9919.@cluster0.nywpd.mongodb.net/")
database = connection["agenda"]
columna = database["contactos"]