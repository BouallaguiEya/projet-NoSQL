from neo4j import GraphDatabase
import csv

# Configuration Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "classe47"
NEO4J_DATABASE = "film"

# Chemins vers les fichiers CSV (dans ton projet)
FILMS_CSV = "data/films.csv"
ACTEURS_CSV = "data/acteurs.csv"

class Neo4jImporter:
    def __init__(self, uri, user, password, database):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def run_query(self, query, params=None):
        with self.driver.session(database=self.database) as session:
            session.run(query, parameters=params or {})

<<<<<<< HEAD
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
=======
    def import_data(self):
        print("🔄 Mise à jour des propriétés des films...")
        with open(FILMS_CSV, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                query = """
>>>>>>> efb121d1bc2b8d1d69703d0920bb05eabc686d02
                MERGE (f:Film {id: $id})
                SET f.title = $title,
                    f.year = toInteger($year),
                    f.votes = toInteger($votes),
                    f.revenue = toFloat($revenue),
                    f.rating = $rating,
                    f.director = $director
                """
                params = {
                    "id": row["id"],
                    "title": row["titre"],
                    "year": row["annee"],
                    "votes": row["votes"],
                    "revenue": row["revenue"],
                    "rating": row["rating"],
                    "director": row["realisateur"]
                }
                self.run_query(query, params)

        print("🎭 Création des relations A_JOUE...")
        with open(ACTEURS_CSV, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                query = """
                MERGE (a:Acteur {name: $acteur})
                MERGE (f:Film {id: $film_id})
                MERGE (a)-[:A_JOUE]->(f)
                """
                params = {
                    "acteur": row["acteur"],
                    "film_id": row["film_id"]
                }
                self.run_query(query, params)

        print(" Importation terminée avec mise à jour des propriétés.")


if __name__ == "__main__":
    importer = Neo4jImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE)
    importer.import_data()
    importer.close()
