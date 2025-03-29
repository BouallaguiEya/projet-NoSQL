from neo4j import GraphDatabase
from config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

def get_neo4j_driver():
    try:
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
        print("Connexion Neo4j réussie")
        return driver
    except Exception as e:
        print(f"Erreur de connexion Neo4j : {e}")
        return None
