import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import csv
from database.mongo_connection import get_mongo_client
from config.config import MONGO_COLLECTION


def exporter_mongo_vers_csv():
    db = get_mongo_client()
    if db is None:
        print(" Problème de connexion à MongoDB.")
        return

    collection = db[MONGO_COLLECTION]
    films = list(collection.find({}, {
        "_id": 1, "title": 1, "year": 1, "votes": 1,
        "revenue": 1, "rating": 1, "director": 1, "actors": 1
    }))

    # Export Films
    with open("data/films.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "titre", "annee", "votes", "revenue", "rating", "realisateur"])
        for film in films:
            writer.writerow([
                str(film.get("_id")),
                film.get("title", ""),
                film.get("year", ""),
                film.get("votes", ""),
                film.get("revenue", ""),
                film.get("rating", ""),
                film.get("director", "")
            ])

    # Export Acteurs (relation A_JOUE)
    with open("data/acteurs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["film_id", "acteur"])
        for film in films:
            film_id = str(film.get("_id"))
            for acteur in film.get("actors", []):
                writer.writerow([film_id, acteur])

    print(" Exportation MongoDB → CSV terminée.")


if __name__ == "__main__":
    exporter_mongo_vers_csv()
