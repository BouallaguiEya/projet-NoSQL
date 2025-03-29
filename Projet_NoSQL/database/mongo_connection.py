from pymongo import MongoClient
from config.config import MONGO_URI, MONGO_DB

def get_mongo_client():
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        print("Connexion MongoDB réussie")
        return db
    except Exception as e:
        print(f"Erreur de connexion MongoDB : {e}")
        return None
