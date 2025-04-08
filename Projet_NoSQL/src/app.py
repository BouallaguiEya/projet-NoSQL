import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mongo_queries import *
import importlib
from cypher_queries import run_query  

st.set_page_config(layout="wide", page_title="Projet NoSQL", page_icon="🎬")
st.title("🎬 Exploration et Interrogation de Bases de Donnees NoSQL")

# Style CSS
st.markdown("""
<style>
    .st-emotion-cache-1kyxreq {justify-content: center;}
    .reportview-container .main .block-container {padding-top: 2rem;}
    h2 {color: #2a9d8f; border-bottom: 2px solid #2a9d8f; padding-bottom: 0.3rem;}
    .stDataFrame {margin-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

# Fonctions Streamlit
def display_ann_plus_grand_nbr_films():
    st.header("1. Année avec le plus grand nombre de films")
    result = ann_plus_grand_nbr_films()
    st.write(result['_id'])
    if result is not None and len(result) > 0:
        col1, col2 = st.columns(2)
        col1.metric("Année record", result['_id'])
        col2.metric("Nombre de films", result['count'])
    else:
        st.warning("Aucun résultat trouvé")

def display_films_apres_1999():
    st.header("2. Nombre de films après 1999")
    count = films_apres_1999()
    st.metric("Nombre de films", count)

def display_moy_votes_2007():
    st.header("3. Moyenne des votes en 2007")
    result = moy_votes_2007()
    if result:
        st.metric("Moyenne des votes", result)
    else:
        st.warning("Aucune donnée disponible")


def display_nbr_films_par_annee():
    st.header("4. Nombre de films par année")
    result = nbr_films_par_annee()
    
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Année", "count": "Nombre"})
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df, x="Année", y="Nombre", ax=ax, palette="viridis")
        plt.xticks(rotation=45, ha='right')
        plt.title("Nombre de films sortis par année")
        st.pyplot(fig)
        
        with st.expander("Voir les données brutes"):
            st.dataframe(df)
    else:
        st.warning("Aucune donnée disponible")

def display_genre_films_dispo():
    st.header("5. Genres disponibles")
    genres = genre_films_dispo()
    if genres:
        st.write("Genres disponibles dans la collection :")
        for genre in genres:
            st.write(f"- {genre}")
    else:
        st.warning("Aucun genre disponible")

def display_film_plus_revenu():
    st.header("6. Film le plus rentable")
    result = film_plus_revenu()
    if result:
        col1, col2 = st.columns(2)
        col1.metric("Titre", result.get('title', 'Inconnu'))
        col2.metric("Revenu", f"${result.get('Revenue (Millions)', 0):.2f}M")
        
        with st.expander("Détails"):
            st.json(result)
    else:
        st.warning("Aucun film avec revenu trouvé")


def display_realisateurs_plus_5_films():
    st.header("7. Réalisateurs avec plus de 5 films")
    result = realisateurs_plus_5_films()
    
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Réalisateur", "count": "Nombre de films"})
        st.dataframe(df)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x="Réalisateur", y="Nombre de films", ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.warning("Aucun réalisateur ayant realise plus de 5 films")
        result2 = realisateurs_plus_3_films()
        st.write("Réalisateurs avec plus de 3 films")
        if result2:
            df = pd.DataFrame(result2).rename(columns={"_id": "Réalisateur", "count": "Nombre de films"})
            st.dataframe(df)
        else:
             st.warning("Aucun réalisateur trouvé")

def display_genre_plus_revenu_moyen():
    st.header("8. Genre rapportant en moyenne le plus de revenu")
    result = genre_plus_revenu_moyen()
    if result:
        st.metric("Genre", result[0]['_id'])
        st.metric("Revenu moyen", f"${result[0]['revenu_moyen']:.2f}M")
    else:
        st.warning("Aucun résultat trouvé")

def display_top_3_decennie():
    st.header("9. Top 3 films par décennie")
    result = top_3_films_par_decennie()
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Décennie", "top3": "Top 3 Films"})
        st.dataframe(df)
    else:
        st.warning("Aucun résultat trouvé")

def display_films_plus_longs():
    st.header("10. Films les plus longs par genre")
    result = film_plus_long_par_genre()
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Genre", "film": "Film", "Runtime (Minutes)": "Durée"})
        st.dataframe(df)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x="Genre", y="Durée", ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.warning("Aucun film trouvé")

def display_creer_vue_films_bien_notes_revenus():
    st.header("11. Films avec une note > 80 et un revenu > 50M")
    result = creer_vue_films_notes_revenus()
    if result:
        df = pd.DataFrame(result).rename(columns={"title": "Titre", "Metascore": "Note", "Revenue (Millions)": "Revenu"})
        st.dataframe(df)
    else:
        st.warning("Aucun film trouvé")

def display_correlation_runtime_revenue():
    st.header("12. Corrélation entre durée et revenu")
    result = correlation_runtime_revenue()  
    if result: 
        st.metric("Correlation", result)
        if result > 0.7:
            st.write("La corrélation est très forte et positive.")
        elif result > 0.3:
            st.write("La corrélation est plutot modérée et positive.")
        elif result < -0.3:
            st.write("La corrélation est plutot modérée et négative.")
        elif result < -0.7:
            st.write("La corrélation est très forte et négative.")
        else:
            st.write("La corrélation est faible.")
    else:
        st.warning("Aucune donnée disponible")
        

def display_evolution_duree_par_decennie():
    st.header("13. Évolution de la durée moyenne des films par décennie")
    result = evolution_duree_par_decennie()
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Décennie", "duree_moyenne": "Durée moyenne"})
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x="Décennie", y="Durée moyenne", ax=ax)
        plt.title("Évolution de la durée moyenne des films par décennie")
        st.pyplot(fig)
    else:
        st.warning("Aucune donnée disponible")

def display_acteur_plus_de_films():
    st.header("14. Acteur ayant joué dans le plus de films")
    query = """
        MATCH (a:Acteur)-[:A_JOUE]->(f:Film)
        RETURN a.name AS acteur, COUNT(f) AS nb_films
        ORDER BY nb_films DESC LIMIT 1
    """
    result = run_query(query)
    if result:
        acteur = result[0]['acteur']
        nb_films = result[0]['nb_films']
        st.metric("Acteur", acteur)
        st.metric("Nombre de films", nb_films)
    else:
        st.warning("Aucun acteur trouvé.")

def display_acteurs_avec_anne_hathaway():
    st.header("15. Acteurs ayant joué avec Anne Hathaway")
    query = """
        MATCH (a1:Acteur {name: 'Anne Hathaway'})-[:A_JOUE]->(f:Film)<-[:A_JOUE]-(a2:Acteur)
        WHERE a1 <> a2
        RETURN DISTINCT a2.name AS acteur
    """
    result = run_query(query)
    if result:
        acteurs = [record['acteur'] for record in result]
        df = pd.DataFrame(acteurs, columns=["Acteur"])
        st.dataframe(df)
    else:
        st.warning("Aucun acteur trouvé.")

def display_acteur_plus_revenus():
    st.header("16. Acteur ayant joué dans les films avec le plus de revenus cumulés")
    query = """
        MATCH (a:Acteur)-[:A_JOUE]->(f:Film)
        RETURN a.name AS acteur, SUM(f.revenue) AS total_revenus
        ORDER BY total_revenus DESC LIMIT 1
    """
    result = run_query(query)
    if result:
        acteur = result[0]['acteur']
        total_revenus = result[0]['total_revenus']
        st.metric("Acteur", acteur)
        st.metric("Total des revenus", f"${total_revenus:.2f}M")
    else:
        st.warning("Aucun acteur trouvé.")

def display_moyenne_votes():
    st.header("17. Moyenne des votes de tous les films")
    query = """
        MATCH (f:Film)
        RETURN avg(f.votes) AS moyenne_votes
    """
    result = run_query(query)
    if result:
        moyenne_votes = result[0]['moyenne_votes']
        st.metric("Moyenne des votes", moyenne_votes)
    else:
        st.warning("Aucune donnée disponible.")

def display_genre_le_plus_represente():
    st.header("18. Genre le plus représenté")
    query = """
        MATCH (f:Film)-[:GENRE]->(g:Genre)
        RETURN g.name AS genre, COUNT(*) AS total
        ORDER BY total DESC LIMIT 1
    """
    result = run_query(query)
    if result:
        genre = result[0]['genre']
        total = result[0]['total']
        st.metric("Genre", genre)
        st.metric("Nombre de films", total)
    else:
        st.warning("Aucun genre trouvé.")

def display_films_avec_coacteurs():
    st.header("19. Films où les co-acteurs des membres du projet ont joué")
    query = """
        MATCH (m:Acteur)-[:A_JOUE]->(f1:Film)<-[:A_JOUE]-(co:Acteur)-[:A_JOUE]->(f2:Film)
        WHERE m.name IN ['Eya BOUALLAGUI', 'Coralie TADJIFOUE'] AND NOT (m)-[:A_JOUE]->(f2)
        RETURN DISTINCT f2.title AS film
        LIMIT 10
    """
    result = run_query(query)
    if result:
        films = [record['film'] for record in result]
        df = pd.DataFrame(films, columns=["Films"])
        st.dataframe(df)
    else:
        st.warning("Aucun film trouvé.")

def display_realisateur_plus_nb_acteurs():
    st.header("20. Réalisateur ayant travaillé avec le plus grand nombre d’acteurs")
    query = """
        MATCH (r:Realisateur)-[:A_REALISE]->(f:Film)<-[:A_JOUE]-(a:Acteur)
        RETURN r.name AS realisateur, COUNT(DISTINCT a) AS nb_acteurs
        ORDER BY nb_acteurs DESC LIMIT 1
    """
    result = run_query(query)
    if result:
        realisateur = result[0]['realisateur']
        nb_acteurs = result[0]['nb_acteurs']
        st.metric("Réalisateur", realisateur)
        st.metric("Nombre d'acteurs", nb_acteurs)
    else:
        st.warning("Aucun réalisateur trouvé.")

def display_films_connus():
    st.header("21. Films les plus connectés (acteurs en commun)")
    query = """
        MATCH (f1:Film)<-[:A_JOUE]-(a:Acteur)-[:A_JOUE]->(f2:Film)
        WHERE f1 <> f2
        RETURN f1.title AS film1, f2.title AS film2, COUNT(DISTINCT a) AS nb_acteurs_communs
        ORDER BY nb_acteurs_communs DESC LIMIT 5
    """
    result = run_query(query)
    if result:
        df = pd.DataFrame(result).rename(columns={"film1": "Film 1", "film2": "Film 2", "nb_acteurs_communs": "Nombre d'acteurs communs"})
        st.dataframe(df)
    else:
        st.warning("Aucun film trouvé.")

def display_top_5_acteurs():
    st.header("22. Top 5 acteurs avec le plus de realisateurs differents")
    query = """
        MATCH (a:Acteur)-[:A_JOUE]->(f:Film)<-[:A_REALISE]-(r:Realisateur)
        RETURN a.name AS acteur, COUNT(DISTINCT r) AS nb_realisateurs
        ORDER BY nb_realisateurs DESC LIMIT 5
    """
    result = run_query(query)
    if result:
        df = pd.DataFrame(result).rename(columns={"acteur": "Acteur", "nb_realisateurs": "Nombre de réalisateurs"})
        st.dataframe(df)
    else:
        st.warning("Aucun acteur trouvé.")

def  display_recommander_anne_hattaway():
    st.header("23. Recommander un film à Anne Hathaway selon ses genres")
    query = """
        MATCH (a:Acteur {name: 'Anne Hathaway'})-[:A_JOUE]->(f:Film)-[:GENRE]->(g:Genre)
        MATCH (rec:Film)-[:GENRE]->(g)
        WHERE NOT (a)-[:A_JOUE]->(rec)
        RETURN DISTINCT rec.title AS recommendation
        LIMIT 5
    """
    result = run_query(query)
    if result:
        recommendations = [record['recommendation'] for record in result]
        df = pd.DataFrame(recommendations, columns=["Recommandations"])
        st.dataframe(df)
    else:
        st.warning("Aucune recommandation trouvée.")

#Chemin le plus court entre Tom Hanks et Scarlett Johansson
def format_chemin_df(result):
    """Transforme le résultat neo4j en df."""
    data = []

    for record in result:
        chemin = record["p"]  

        acteurs = []  

        for elem in chemin:
            if isinstance(elem, dict) and "name" in elem:  
                acteurs.append(elem["name"])

        for i in range(len(acteurs) - 1):
            acteur1 = acteurs[i]
            acteur2 = acteurs[i + 1]
            data.append([acteur1, "A_JOUE_AVEC", acteur2])

    return pd.DataFrame(data, columns=["Acteur 1", "Relation", "Acteur 2"])


def display_chemin_le_plus_court():
    st.header("24. Chemin le plus court entre Tom Hanks et Scarlett Johansson")

    query = """
        MATCH p=shortestPath((a1:Acteur {name:'Tom Hanks'})-[:A_JOUE*]-(a2:Acteur {name:'Scarlett Johansson'}))
        RETURN p
    """
    result = run_query(query)

    if result:
        df = format_chemin_df(result)
        st.write("### Chemin:")
        st.dataframe(df)
    else:
        st.warning("Aucun chemin trouvé.")

# onglet de navigation
st.sidebar.title("Navigation")
options = [
    "1. Année record de sorties",
    "2. Films post-1999",
    "3. Moyenne votes 2007",
    "4. Films par année",
    "5. Genres disponibles",
    "6. Film le plus rentable",
    "7. Réalisateurs ayant realisé plus de 5 films",
    "8. Genre le plus rentable",
    "9. Top 3 par décennie",
    "10. Films les plus longs",
    "11. Films bien notés",
    "12. Corrélation durée-revenu",
    "13. Évolution durée moyenne",
    "14. Acteur ayant joué dans le plus de films",
    "15. Acteurs ayant joué avec Anne Hathaway",
    "16. Acteur avec le plus de revenus",
    "17. Moyenne des votes",
    "18. Genre le plus représenté",
    "19. Films avec co-acteurs",
    "20. Réalisateur avec le plus d'acteurs",
    "21. Films les plus connectés",
    "22. Top 5 acteurs avec le plus de réalisateurs",
    "23. Recommander un film à Anne Hathaway",
    "24. Chemin le plus court entre Tom Hanks et Scarlett Johansson"
]
choice = st.sidebar.selectbox('Choisir une option', options)

# Options
if choice == options[0]:
    display_ann_plus_grand_nbr_films()
elif choice == options[1]:
    display_films_apres_1999()
elif choice == options[2]:
    display_moy_votes_2007()
elif choice == options[3]:
    display_nbr_films_par_annee()
elif choice == options[4]:
    display_genre_films_dispo()
elif choice == options[5]:
    display_film_plus_revenu()
elif choice == options[6]:
    display_realisateurs_plus_5_films()
elif choice == options[7]:
    display_genre_plus_revenu_moyen()
elif choice == options[8]:
    display_top_3_decennie()
elif choice == options[9]:
    display_films_plus_longs()
elif choice == options[10]:
    display_creer_vue_films_bien_notes_revenus()
elif choice == options[11]:
    display_correlation_runtime_revenue()
elif choice == options[12]:
    display_evolution_duree_par_decennie()
elif choice == options[13]:
    display_acteur_plus_de_films()
elif choice == options[14]:
    display_acteurs_avec_anne_hathaway()
elif choice == options[15]:
    display_acteur_plus_revenus()
elif choice == options[16]:
    display_moyenne_votes()
elif choice == options[17]:
    display_genre_le_plus_represente()
elif choice == options[18]:
    display_films_avec_coacteurs()
elif choice == options[19]:
    display_realisateur_plus_nb_acteurs()
elif choice == options[20]:
    display_films_connus()
elif choice == options[21]:
    display_top_5_acteurs()
elif choice == options[22]:
    display_recommander_anne_hattaway()
elif choice == options[23]:
    display_chemin_le_plus_court()
else:
    st.warning("Sélectionnez une option valide")


st.divider()
st.caption("Projet NoSQL • TADJIFOUE BOUALLAHUI • 2025")