import sys
import os
import csv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mongo_connection import get_mongo_client
from config.config import MONGO_COLLECTION


def exporter_mongo_vers_csv():
    db = get_mongo_client()
    if db is None:
        print("Problème de connexion à MongoDB.")
        return

    collection = db[MONGO_COLLECTION]
    films = list(collection.find({}, {
        "_id": 1, "title": 1, "year": 1, "Votes": 1,
        "Revenue (Millions)": 1, "rating": 1, "Director": 1, "Actors": 1
    }))

    # Export Films
    os.makedirs("data", exist_ok=True)
    with open("data/films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "titre", "annee", "votes", "revenue", "rating", "realisateur"])
        for film in films:
            writer.writerow([
                str(film.get("_id")),
                film.get("title", ""),
                film.get("year", ""),
                film.get("Votes", ""),
                film.get("Revenue (Millions)", ""),
                film.get("rating", ""),
                film.get("Director", "")
            ])

    # Export Acteurs (relation A_JOUE)
    with open("data/acteurs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["film_id", "acteur"])
        for film in films:
            film_id = str(film.get("_id"))
            acteurs = film.get("Actors", "")
            if acteurs:
                for acteur in [a.strip() for a in acteurs.split(",")]:
                    writer.writerow([film_id, acteur])

    print("✅ Exportation MongoDB → CSV terminée.")


if __name__ == "__main__":
    exporter_mongo_vers_csv()
