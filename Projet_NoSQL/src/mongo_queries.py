import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mongo_connection import get_mongo_client
from config.config import MONGO_COLLECTION

def get_collection():
    db = get_mongo_client()
    if db is not None:
        return db[MONGO_COLLECTION]
    else:
        print("Impossible de récupérer la collection MongoDB")
        return None

# 1-Année avec le plus grand nombre de films
def ann_plus_grand_nbr_films():
    collection = get_collection()
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    if result:
        print(f"Année avec le plus grand nombre de films : {result[0]['_id']} ({result[0]['count']} films)")
    else:
        print("Aucune donnée disponible.")

# 2-Nombre de films après 1999
def films_apres_1999():
    collection = get_collection()
    count = collection.count_documents({"year": {"$gt": 1999}})
    print(f"Nombre de films après 1999 : {count}")

# 3-Moyenne des votes des films sortis en 2007
def moy_votes_2007():
    collection = get_collection()
    pipeline = [
        {"$match": {"year": 2007}},
        {"$group": {"_id": None, "average_votes": {"$avg": "$votes"}}}
    ]
    result = list(collection.aggregate(pipeline))
    if result and result[0]["average_votes"] is not None:
        moyenne = result[0]["average_votes"]
        print(f"Moyenne des votes en 2007 : {moyenne:.2f}")
    else:
        print("Aucun film trouvé pour l'année 2007.")

# 4-Nombre de films par année
def nbr_films_par_annee():
    collection = get_collection()
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    for item in result:
        print(f"Année : {item['_id']} - Nombre de films : {item['count']}")

# 5-Genres de films disponibles
def genre_films_dispo():
    collection = get_collection()
    genres = collection.distinct("genre")
    print(f"Genres de films disponibles : {genres}")

# 6-Film ayant généré le plus de revenu
def film_plus_revenu():
    collection = get_collection()
    result = collection.find_one({"revenue": {"$exists": True, "$ne": None}}, sort=[("revenue", -1)])
    if result:
        print(f"Film avec le plus de revenu : {result.get('title', 'Inconnu')} ({result.get('revenue', 'Non renseigné')}$)")
    else:
        print("Aucun film avec un revenu renseigné trouvé.")

# 7-Réalisateurs ayant réalisé plus de 5 films
def realisateurs_plus_5_films():
    collection = get_collection()
    pipeline = [
        {"$match": {"director": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}}
    ]
    result = list(collection.aggregate(pipeline))
    if result:
        for r in result:
            print(f"Réalisateur : {r['_id']} - Nombre de films : {r['count']}")
    else:
        print("Aucun réalisateur avec plus de 5 films trouvé.")

# 8-Genre rapportant en moyenne le plus de revenus
def genre_plus_revenu_moyen():
    collection = get_collection()
    pipeline = [
        {"$match": {"revenue": {"$exists": True, "$ne": None}, "genre": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$genre", "revenu_moyen": {"$avg": "$revenue"}}},
        {"$sort": {"revenu_moyen": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    if result:
        print(f"Genre avec revenu moyen le plus élevé : {result[0]['_id']} ({result[0]['revenu_moyen']}$)")
    else:
        print("Aucun genre avec revenu disponible.")

# 9-3 films les mieux notés par décennie
def top_3_films_par_decennie():
    collection = get_collection()
    pipeline = [
        {"$match": {"title": {"$exists": True, "$ne": None}, "rating": {"$exists": True, "$ne": None}, "year": {"$exists": True, "$ne": None}}},
        {"$project": {
            "title": 1,
            "rating": 1,
            "decennie": {"$concat": [
                {"$toString": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}},
                "-",
                {"$toString": {"$add": [
                    {"$subtract": ["$year", {"$mod": ["$year", 10]}]},
                    9
                ]}}
            ]}
        }},
        {"$sort": {"decennie": 1, "rating": -1}},
        {"$group": {
            "_id": "$decennie",
            "films": {"$push": {"title": "$title", "rating": "$rating"}}
        }},
        {"$project": {"_id": 1, "top3": {"$slice": ["$films", 3]}}}
    ]
    result = list(collection.aggregate(pipeline))
    for r in result:
        print(f"Décennie : {r['_id']}")
        for film in r["top3"]:
            print(f"  - {film.get('title', 'Titre inconnu')} (rating : {film.get('rating', 'non renseigné')})")

# 10-Film le plus long par genre
def film_plus_long_par_genre():
    collection = get_collection()
    pipeline = [
        {"$match": {"runtime": {"$exists": True, "$ne": None}, "genre": {"$exists": True, "$ne": None}}},
        {"$sort": {"runtime": -1}},
        {"$group": {
            "_id": "$genre",
            "film": {"$first": "$title"},
            "runtime": {"$first": "$runtime"}
        }}
    ]
    result = list(collection.aggregate(pipeline))
    for r in result:
        print(f"Genre : {r['_id']} - Film : {r['film']} ({r['runtime']} min)")

# 11-Vue MongoDB : films avec note > 80 et revenu > 50M
def creer_vue_films_notes_revenus():
    collection = get_collection()
    pipeline = [
        {"$match": {"metascore": {"$gt": 80}, "revenue": {"$gt": 50000000}}},
        {"$project": {"title": 1, "metascore": 1, "revenue": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    if result:
        print("Films avec Metascore > 80 et revenu > 50M :")
        for film in result:
            print(f"- {film['title']} (Metascore : {film['metascore']}, Revenu : {film['revenue']}$)")
    else:
        print("Aucun film correspondant trouvé.")

# 12- Corrélation entre runtime et revenu
def correlation_runtime_revenue():
    collection = get_collection()
    data = list(collection.find(
        {"runtime": {"$exists": True, "$ne": None}, "revenue": {"$exists": True, "$ne": None}},
        {"runtime": 1, "revenue": 1, "_id": 0}
    ))
    if not data:
        print("Aucune donnée disponible pour calculer la corrélation.")
        return

    df = pd.DataFrame(data)
    if "runtime" in df.columns and "revenue" in df.columns:
        correlation = df["runtime"].corr(df["revenue"])
        if pd.notnull(correlation):
            print(f"Corrélation entre durée et revenu : {correlation:.2f}")
        else:
            print("Impossible de calculer la corrélation (valeurs manquantes).")
    else:
        print("Colonnes nécessaires absentes pour le calcul.")
# 13- Évolution de la durée moyenne des films par décennie
def evolution_duree_par_decennie():
    collection = get_collection()
    pipeline = [
        {"$match": {"runtime": {"$exists": True, "$ne": None}, "year": {"$exists": True, "$ne": None}}},
        {"$project": {
            "runtime": 1,
            "decennie": {"$concat": [
                {"$toString": {"$subtract": ["$year", {"$mod": ["$year", 10]}]}},
                "-",
                {"$toString": {"$add": [
                    {"$subtract": ["$year", {"$mod": ["$year", 10]}]},
                    9
                ]}}
            ]}
        }},
        {"$group": {
            "_id": "$decennie",
            "duree_moyenne": {"$avg": "$runtime"}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    if result:
        for r in result:
            print(f"Décennie : {r['_id']} - Durée moyenne : {r['duree_moyenne']:.2f} min")
    else:
        print("Aucune donnée disponible pour calculer l'évolution.")

# Test local
if __name__ == "__main__":
    ann_plus_grand_nbr_films()
    films_apres_1999()
    moy_votes_2007()
    nbr_films_par_annee()
    genre_films_dispo()
    film_plus_revenu()
    realisateurs_plus_5_films()
    genre_plus_revenu_moyen()
    top_3_films_par_decennie()
    film_plus_long_par_genre()
    creer_vue_films_notes_revenus()
    correlation_runtime_revenue()
    evolution_duree_par_decennie()

