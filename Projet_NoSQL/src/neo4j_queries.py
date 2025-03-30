import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.neo4j_connection import get_neo4j_driver
from database.mongo_connection import get_mongo_client
from config.config import MONGO_COLLECTION

# 1- Créer les noeuds Film
def films():
    driver = get_neo4j_driver()
    db = get_mongo_client()
    if driver is None or db is None:
        return

    collection = db[MONGO_COLLECTION]
    films = collection.find({}, {"_id": 1, "title": 1, "year": 1, "votes": 1, "revenue": 1, "rating": 1, "director": 1})

    with driver.session() as session:
        for film in films:
            session.run("""
            CREATE (f:Film {
                id: $id,
                titre: $titre,
                annee: $annee,
                votes: $votes,
                revenue: $revenue,
                rating: $rating,
                realisateur: $realisateur
            })
            """, {
                "id": str(film.get("_id")),
                "titre": film.get("title"),
                "annee": film.get("year"),
                "votes": film.get("votes"),
                "revenue": film.get("revenue"),
                "rating": film.get("rating"),
                "realisateur": film.get("director")
            })
    print("Nœuds Film créés avec succès.")

# 2- Créer les noeuds Actors
def actors():
    driver = get_neo4j_driver()
    db = get_mongo_client()
    if driver is None or db is None:
        return

    collection = db[MONGO_COLLECTION]
    acteurs = set()
    for film in collection.find({}, {"actors": 1}):
        if "actors" in film:
            acteurs.update(film["actors"])

    with driver.session() as session:
        for acteur in acteurs:
            session.run("""
            CREATE (:Acteur {nom: $nom})
            """, {"nom": acteur})
    print("Nœuds Acteur créés avec succès.")

# 3- Créer les relations A_JOUE
def relations_a_jouer():
    driver = get_neo4j_driver()
    db = get_mongo_client()
    if driver is None or db is None:
        return

    collection = db[MONGO_COLLECTION]
    with driver.session() as session:
        for film in collection.find({}, {"_id": 1, "actors": 1}):
            film_id = str(film.get("_id"))
            if "actors" in film:
                for acteur in film["actors"]:
                    session.run("""
                    MATCH (a:Acteur {nom: $nom}), (f:Film {id: $film_id})
                    CREATE (a)-[:A_JOUE]->(f)
                    """, {"nom": acteur, "film_id": film_id})
    print("Relations A_JOUE créées avec succès.")

# 4- Créer les noeuds Actors pour les membres du projet
def membres_projet():
    driver = get_neo4j_driver()
    if driver is None:
        return

    membres = ["Membre1", "Membre2", "Membre3"]
    with driver.session() as session:
        for membre in membres:
            session.run("""
            CREATE (:Acteur {nom: $nom})
            """, {"nom": membre})

        # Attacher à un film arbitraire (par exemple avec id existant)
        film_id = "1"
        for membre in membres:
            session.run("""
            MATCH (a:Acteur {nom: $nom}), (f:Film {id: $film_id})
            CREATE (a)-[:A_JOUE]->(f)
            """, {"nom": membre, "film_id": film_id})
    print("Membres du projet ajoutés et liés à un film.")

# 5- Créer les noeuds Realisateur
def realisateurs():
    driver = get_neo4j_driver()
    db = get_mongo_client()
    if driver is None or db is None:
        return

    collection = db[MONGO_COLLECTION]
    realisateurs = set()
    for film in collection.find({}, {"director": 1}):
        if film.get("director"):
            realisateurs.add(film["director"])

    with driver.session() as session:
        for realisateur in realisateurs:
            session.run("""
            CREATE (:Realisateur {nom: $nom})
            """, {"nom": realisateur})
    print("Nœuds Realisateur créés avec succès.")

# Test local
if __name__ == "__main__":
    films()
    actors()
    relations_a_jouer()
    membres_projet()
    realisateurs()