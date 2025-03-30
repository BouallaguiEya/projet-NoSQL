from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "classe47"
NEO4J_DATABASE = "film"


def run_query(query, params=None):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run(query, parameters=params or {})
        return [record.data() for record in result]


if __name__ == "__main__":
    print("14. Acteur ayant joué dans le plus de films :")
    print(run_query("""
        MATCH (a:Acteur)-[:A_JOUE]->(f:Film)
        RETURN a.name AS acteur, COUNT(f) AS nb_films
        ORDER BY nb_films DESC LIMIT 1
    """))

    print("15. Acteurs ayant joué avec Anne Hathaway :")
    print(run_query("""
        MATCH (a1:Acteur {name: 'Anne Hathaway'})-[:A_JOUE]->(f:Film)<-[:A_JOUE]-(a2:Acteur)
        WHERE a1 <> a2
        RETURN DISTINCT a2.name AS acteur
    """))

    print("16. Acteur ayant joué dans les films avec le plus de revenus cumulés :")
    print(run_query("""
        MATCH (a:Acteur)-[:A_JOUE]->(f:Film)
        RETURN a.name AS acteur, SUM(f.revenue) AS total_revenus
        ORDER BY total_revenus DESC LIMIT 1
    """))

    print("17. Moyenne des votes de tous les films :")
    print(run_query("""
        MATCH (f:Film)
        RETURN avg(f.votes) AS moyenne_votes
    """))

    print("18. Genre le plus représenté :")
    print(run_query("""
        MATCH (f:Film)-[:GENRE]->(g:Genre)
        RETURN g.name AS genre, COUNT(*) AS total
        ORDER BY total DESC LIMIT 1
    """))

    print("19. Films où les co-acteurs des membres du projet ont joué :")
    print(run_query("""
        MATCH (m:Acteur)-[:A_JOUE]->(f1:Film)<-[:A_JOUE]-(co:Acteur)-[:A_JOUE]->(f2:Film)
        WHERE m.name IN ['Eya BOUALLAGUI', 'Coralie TADJIFOUE'] AND NOT (m)-[:A_JOUE]->(f2)
        RETURN DISTINCT f2.title AS film
        LIMIT 10
    """))

    print("20. Réalisateur ayant travaillé avec le plus grand nombre d’acteurs :")
    print(run_query("""
        MATCH (r:Realisateur)-[:A_REALISE]->(f:Film)<-[:A_JOUE]-(a:Acteur)
        RETURN r.name AS realisateur, COUNT(DISTINCT a) AS nb_acteurs
        ORDER BY nb_acteurs DESC LIMIT 1
    """))

    print("21. Films les plus connectés (acteurs en commun) :")
    print(run_query("""
        MATCH (f1:Film)<-[:A_JOUE]-(a:Acteur)-[:A_JOUE]->(f2:Film)
        WHERE f1 <> f2
        RETURN f1.title AS film1, f2.title AS film2, COUNT(DISTINCT a) AS nb_acteurs_communs
        ORDER BY nb_acteurs_communs DESC LIMIT 5
    """))

    print("22. Top 5 acteurs ayant joué avec le plus de réalisateurs différents :")
    print(run_query("""
        MATCH (a:Acteur)-[:A_JOUE]->(f:Film)<-[:A_REALISE]-(r:Realisateur)
        RETURN a.name AS acteur, COUNT(DISTINCT r) AS nb_realisateurs
        ORDER BY nb_realisateurs DESC LIMIT 5
    """))

    print("23. Recommander un film à Anne Hathaway selon ses genres :")
    print(run_query("""
        MATCH (a:Acteur {name: 'Anne Hathaway'})-[:A_JOUE]->(f:Film)-[:GENRE]->(g:Genre)
        MATCH (rec:Film)-[:GENRE]->(g)
        WHERE NOT (a)-[:A_JOUE]->(rec)
        RETURN DISTINCT rec.title AS recommendation
        LIMIT 5
    """))

    print("24. Créer les relations INFLUENCE_PAR entre réalisateurs (genres en commun) :")
    run_query("""
        MATCH (r1:Realisateur)-[:A_REALISE]->(:Film)-[:GENRE]->(g:Genre)<-[:GENRE]-(:Film)<-[:A_REALISE]-(r2:Realisateur)
        WHERE r1 <> r2
        MERGE (r1)-[:INFLUENCE_PAR]->(r2)
    """)
    print("✅ Relations INFLUENCE_PAR créées.")

    print("25. Chemin le plus court entre Tom Hanks et Scarlett Johansson :")
    print(run_query("""
        MATCH p=shortestPath((a1:Acteur {name:'Tom Hanks'})-[:A_JOUE*]-(a2:Acteur {name:'Scarlett Johansson'}))
        RETURN p
    """))

    
