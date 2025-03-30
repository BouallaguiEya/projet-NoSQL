import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import csv
from database.mongo_connection import get_mongo_client

def exporter_relations_correct():
    db = get_mongo_client()
    collection = db["films"]

    relations = []
    for film in collection.find({"Actors": {"$exists": True, "$ne": ""}}, {"title": 1, "Actors": 1, "_id": 0}):
        acteurs = film["Actors"].split(",")  # Séparation de la chaîne
        for acteur in acteurs:
            relations.append({
                "film": film["title"],
                "actor": acteur.strip()
            })

    if not relations:
        print("Aucune relation trouvée.")
        return

    # Export CSV
    with open("data/relations.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["film", "actor"])
        writer.writeheader()
        writer.writerows(relations)

    print(f"Exportation de {len(relations)} relations film/acteur terminée.")

if __name__ == "__main__":
    exporter_relations_correct()

