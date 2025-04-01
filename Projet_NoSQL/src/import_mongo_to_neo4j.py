import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from database.mongo_connection import get_mongo_client
from database.neo4j_connection import get_neo4j_driver
from config.config import MONGO_COLLECTION


def get_films_mongo():
    db = get_mongo_client()
    if db is not None:
        collection = db[MONGO_COLLECTION]
        films = list(collection.find({}, {
            "_id": 1, "title": 1, "year": 1, "Votes": 1,
            "Revenue (Millions)": 1,  
            "rating": 1, "director": 1, "actors": 1
        }))
        
        
        for film in films:
            film["votes"] = film.pop("Votes", None)  
            film["revenue"] = film.pop("Revenue (Millions)", None)
            film["annee"] = film.pop("year", 0000)  
            film["titre"] = film.pop("title", "Titre inconnu")
        return films
    return []


def importer_donnees_neo4j():
    driver = get_neo4j_driver()
    films = get_films_mongo()

    if driver is None or not films:
        print(" Problème de connexion ou données vides.")
        return

    with driver.session(database="neo4j") as session:
        for film in films:
            session.run("""
                MERGE (f:Film {
                    id: $id,
                    titre: $titre,
                    annee: $annee,
                    votes: $votes,
                    revenue: $revenue,
                    rating: $rating
                })
            """, {
                "id": str(film.get("_id")),
                "titre": film.get("title"),
                "annee": film.get("year"),
                "votes": film.get("votes"),
                "revenue": film.get("revenue"),
                "rating": film.get("rating")
            })

            # Réalisateur
            realisateur = film.get("director")
            if realisateur:
                session.run("""
                    MERGE (r:Realisateur {nom: $nom})
                    MATCH (f:Film {id: $id})
                    MERGE (r)-[:REALISE]->(f)
                """, {
                    "nom": realisateur,
                    "id": str(film.get("_id"))
                })

            # Acteurs
            acteurs = film.get("actors", [])
            for acteur in acteurs:
                session.run("""
                    MERGE (a:Acteur {nom: $nom})
                    MATCH (f:Film {id: $id})
                    MERGE (a)-[:A_JOUE]->(f)
                """, {
                    "nom": acteur,
                    "id": str(film.get("_id"))
                })

    print("Importation MongoDB → Neo4j terminée.")


if __name__ == "__main__":
    importer_donnees_neo4j()
