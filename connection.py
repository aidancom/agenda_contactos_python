import pymongo, os
from dotenv import load_dotenv

load_dotenv()
connection = pymongo.MongoClient(f"mongodb+srv://root:{os.getenv('DATABASE_KEY')}@cluster0.nywpd.mongodb.net/")
database = connection["agenda"]

columna = database["contactos"]
columna_2 = database['estilos']
columna_3 = database['eliminados']