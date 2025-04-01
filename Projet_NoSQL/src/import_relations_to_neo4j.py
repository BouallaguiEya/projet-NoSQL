import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neo4j import GraphDatabase
from pymongo import MongoClient

# Configuration MongoDB
MONGO_URI = "mongodb+srv://classe47:classe47@esiea47.vhmvb3q.mongodb.net/?retryWrites=true&w=majority&appName=esiea47"
MONGO_DB = "entertainment"
MONGO_COLLECTION = "films"

# Configuration Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "classe47"
NEO4J_DATABASE = "film"

# Membres du projet
MEMBRES_PROJET = ["Eya BOUALLAGUI", "Coralie TADJIFOUE"]


def get_mongo_data():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    films = list(collection.find())
    return films


def get_neo4j_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def insert_data():
    films = get_mongo_data()
    driver = get_neo4j_driver()

    with driver.session(database=NEO4J_DATABASE) as session:
        # Nettoyage de la base
        session.run("MATCH (n) DETACH DELETE n")

        for film in films:
            film_id = str(film.get('_id'))
            title = film.get('title')
            year = film.get('year')
            votes = film.get('Votes')
            revenue = film.get('Revenue (Millions)', 0.0)
            if isinstance(revenue, str):
                revenue = 0.0
            rating = film.get('rating')
            director = film.get('Director')
            actors_raw = film.get('Actors', "")
            genres_raw = film.get('genre')

            if not film_id or not title:
                continue

            # Nettoyage acteurs
            actors = [a.strip() for a in actors_raw.split(",") if a.strip()]

            # Nettoyage genres
            genres = []
            if isinstance(genres_raw, str):
                genres = [g.strip() for g in genres_raw.split(",") if g.strip()]
            elif isinstance(genres_raw, list):
                genres = genres_raw

            # Créer le noeud Film
            session.run("""
                MERGE (f:Film {id: $id})
                SET f.title = $title, f.year = $year, f.votes = $votes, f.revenue = $revenue, f.rating = $rating
            """, id=film_id, title=title, year=year, votes=votes, revenue=revenue, rating=rating)

            # Créer le noeud Realisateur
            if director:
                session.run("""
                    MERGE (r:Realisateur {name: $name})
                    MERGE (f:Film {id: $id})
                    MERGE (r)-[:A_REALISE]->(f)
                """, name=director, id=film_id)

            # Créer les noeuds Acteur + relation A_JOUE
            for actor in actors:
                session.run("""
                    MERGE (a:Acteur {name: $name})
                    MERGE (f:Film {id: $id})
                    MERGE (a)-[:A_JOUE]->(f)
                """, name=actor, id=film_id)

            # Créer les noeuds Genre + relation GENRE
            for genre in genres:
                session.run("""
                    MERGE (g:Genre {name: $name})
                    MERGE (f:Film {id: $id})
                    MERGE (f)-[:GENRE]->(g)
                """, name=genre, id=film_id)

        # Ajouter les membres du projet
        for membre in MEMBRES_PROJET:
            session.run("""
                MERGE (a:Acteur {name: $name})
                MERGE (f:Film {title: 'Avatar'})
                MERGE (a)-[:A_JOUE]->(f)
            """, name=membre)

    driver.close()


if __name__ == "__main__":
    insert_data()
    print("✅ Importation MongoDB → Neo4j terminée avec succès")
