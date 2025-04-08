from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "classe47"
NEO4J_DATABASE = "film"


def run_query(query, params=None, write=False):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session(database=NEO4J_DATABASE) as session:
        if write:
            session.execute_write(lambda tx: tx.run(query, parameters=params or {}))
            return []
        else:
            result = session.run(query, parameters=params or {})
            return [record.data() for record in result]


