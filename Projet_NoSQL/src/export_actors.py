import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from database.mongo_connection import get_mongo_client
import csv

def exporter_acteurs():
    db = get_mongo_client()
    if db is None:
        print("Échec de connexion MongoDB")
        return

    collection = db["films"]
    acteurs_set = set()

    for film in collection.find({"Actors": {"$exists": True, "$ne": ""}}):
        acteurs = film.get("Actors", "").split(",")
        for acteur in acteurs:
            acteurs_set.add(acteur.strip())

    if not acteurs_set:
        print("Aucun acteur trouvé.")
        return

    # Export en CSV
    with open("data/actors.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        for acteur in sorted(acteurs_set):
            writer.writerow([acteur])

    print(f"✅ Exportation de {len(acteurs_set)} acteurs terminée.")

if __name__ == "__main__":
    exporter_acteurs()
