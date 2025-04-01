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
    return result[0] if result else None

# 2-Nombre de films après 1999
def films_apres_1999():
    collection = get_collection() 
    return collection.count_documents({"year": {"$gt": 1999}})

# 3-Moyenne des votes des films sortis en 2007
def moy_votes_2007():
    collection = get_collection()
    pipeline = [
        {"$match": {"year": 2007, "Votes": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": None, "average_votes": {"$avg": "$Votes"}}}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0]['average_votes'] if result else None

# 4-Nombre de films par année
def nbr_films_par_annee():
    collection = get_collection()
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result 

# 5-Genres de films disponibles
def genre_films_dispo():
    collection = get_collection()
    genres = collection.distinct("genre")
    return genres if genres else "Aucun genre disponible"

# 6-Film ayant généré le plus de revenu
def film_plus_revenu():
    collection = get_collection()
    result = collection.find_one({"Revenue (Millions)": {"$exists": True, "$ne": None, "$ne": ''}}, sort=[("Revenue (Millions)", -1)])
    return result

# 7-Réalisateurs ayant réalisé plus de 5 films
def realisateurs_plus_5_films():
    collection = get_collection()
    pipeline = [
        {"$match": {"Director": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 5}}},
        {"$sort": {"count": -1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result 

def realisateurs_plus_3_films():
    collection = get_collection()
    pipeline = [
        {"$match": {"Director": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$Director", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 3}}},
        {"$sort": {"count": -1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result 

# 8-Genre rapportant en moyenne le plus de revenus
def genre_plus_revenu_moyen():
    collection = get_collection()
    pipeline = [
        {"$match": {"Revenue (Millions)": {"$exists": True, "$ne": None}, "genre": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": "$genre", "revenu_moyen": {"$avg": "$Revenue (Millions)"}}},
        {"$sort": {"revenu_moyen": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result

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
    {"$project": {
        "_id": 1,
        "top3": {"$slice": [
            {"$map": {
                "input": "$films",
                "as": "film",
                "in": "$$film.title"
            }},
            3
        ]}
    }}
]

    result = list(collection.aggregate(pipeline))
    return result if result else "Aucun film trouvé"

# 10-Film le plus long par genre
def film_plus_long_par_genre():
    collection = get_collection()
    pipeline = [
        {"$match": {"Runtime (Minutes)": {"$exists": True, "$ne": None}, "genre": {"$exists": True, "$ne": None}}},
        {"$unwind": "$genre"}, 
        {"$sort": {"Runtime (Minutes)": -1}},  
        {"$group": {
            "_id": "$genre", 
            "film": {"$first": "$title"}, 
            "Runtime (Minutes)": {"$first": "$Runtime (Minutes)"}  
        }}
    ]
    result = list(collection.aggregate(pipeline))
    return result


# 11-Vue MongoDB : films avec note > 80 et revenu > 50M
def creer_vue_films_notes_revenus():
    collection = get_collection()
    pipeline = [
        {"$match": {"Metascore": {"$gt": 80}, "Revenue (Millions)": {"$gt": 500}}},
        {"$project": {"title": 1, "Metascore": 1, "Revenue (Millions)": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result

# 12- Corrélation entre runtime et revenu
def correlation_runtime_revenue():
    collection = get_collection()
    data = list(collection.find(
        {"Runtime (Minutes)": {"$exists": True}, "Revenue (Millions)": {"$exists": True, "$ne": ''}}, 
        {"Runtime (Minutes)": 1, "Revenue (Millions)": 1, "_id": 0}
    ))
    if not data:
        return "Aucune donnée disponible"
    
    df = pd.DataFrame(data)
    correlation = df["Runtime (Minutes)"].corr(df["Revenue (Millions)"])
    return correlation if correlation else None

# 13- Évolution de la durée moyenne des films par décennie
def evolution_duree_par_decennie():
    collection = get_collection()
    pipeline = [
        {"$match": {"Runtime (Minutes)": {"$exists": True, "$ne": None}, "year": {"$exists": True, "$ne": None}}},
        {"$project": {
            "Runtime (Minutes)": 1,
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
            "duree_moyenne": {"$avg": "$Runtime (Minutes)"}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(collection.aggregate(pipeline))
    return result if result else None