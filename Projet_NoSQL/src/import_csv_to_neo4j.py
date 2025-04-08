from neo4j import GraphDatabase

# Configuration Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "classe47"
NEO4J_DATABASE = "film"

class Neo4jImporter:
    def __init__(self, uri, user, password, database):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session(database=self.database) as session:
            session.run(query)

    def import_data(self):
        print(" Suppression des anciens nœuds...")
        self.run_query("MATCH (n) DETACH DELETE n")

        print(" Importation des films...")
        import_films = """
        LOAD CSV WITH HEADERS FROM 'file:///films.csv' AS row
        CREATE (f:Film {
            id: row.id,
            title: row.titre,
            year: toInteger(row.annee),
            votes: toInteger(row.votes),
            revenue: toFloat(row.revenue),
            rating: row.rating,
            director: row.realisateur
        });
        """
        self.run_query(import_films)

        print(" Importation des acteurs et relations...")
        import_acteurs = """
        LOAD CSV WITH HEADERS FROM 'file:///acteurs.csv' AS row
        MERGE (a:Acteur {name: row.acteur})
        WITH a, row
        MATCH (f:Film {id: row.film_id})
        MERGE (a)-[:A_JOUE]->(f);
        """
        self.run_query(import_acteurs)

        print(" Importation terminée.")


if __name__ == "__main__":
    importer = Neo4jImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE)
    importer.import_data()
    importer.close()
