import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from database.mongo_connection import get_mongo_client
from config.config import MONGO_COLLECTION
import os

def importer_donnees():
    db = get_mongo_client()
    if db is None:
        print("Connexion MongoDB échouée")
        return

    collection = db[MONGO_COLLECTION]

    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(current_dir, "movies.json")

        data = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                data.append(json.loads(line))

        collection.insert_many(data)
        print(f"{len(data)} films insérés avec succès dans MongoDB.")

    except Exception as e:
        print(f"Erreur lors de l'importation : {e}")

if __name__ == "__main__":
    importer_donnees()
