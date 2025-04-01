import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mongo_queries import *

# Configuration de la page
st.set_page_config(layout="wide", page_title="Analyse de Films", page_icon="🎬")
st.title("🎬 Analyse de la Base de Données de Films")

# Style CSS personnalisé
st.markdown("""
<style>
    .st-emotion-cache-1kyxreq {justify-content: center;}
    .reportview-container .main .block-container {padding-top: 2rem;}
    h2 {color: #2a9d8f; border-bottom: 2px solid #2a9d8f; padding-bottom: 0.3rem;}
    .stDataFrame {margin-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

# Fonctions d'affichage Streamlit
def display_ann_plus_grand_nbr_films():
    st.header("1. Année avec le plus grand nombre de films")
    result = ann_plus_grand_nbr_films()
    if result:
        col1, col2 = st.columns(2)
        col1.metric("Année record", result[0]['_id'])
        col2.metric("Nombre de films", result[0]['count'])
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
        col2.metric("Revenu", f"${result.get('revenue', 0)/1e6:.2f}M")
        
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
        st.warning("Aucun réalisateur trouvé")

def display_genre_plus_revenu_moyen():
    st.header("8. Genre rapportant en moyenne le plus de revenu")
    result = genre_plus_revenu_moyen()
    if result:
        st.metric("Genre", result[0]['_id'])
        st.metric("Revenu moyen", f"${result[0]['revenu_moyen']/1e6:.2f}M")
    else:
        st.warning("Aucun résultat trouvé")

def display_top_3_decennie():
    st.header("9. Top 3 films par décennie")
    result = top_3_films_par_decennie()
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Décennie", "top_films": "Top 3 Films"})
        st.dataframe(df)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df.explode("Top 3 Films"), x="Décennie", y="Top 3 Films", ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.warning("Aucun résultat trouvé")

def display_films_plus_longs():
    st.header("10. Films les plus longs par genre")
    result = film_plus_long_par_genre()
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Genre", "film": "Film", "duree": "Durée"})
        st.dataframe(df)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x="Genre", y="Durée", ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.warning("Aucun film trouvé")

def display_creer_vue_films_bien_notes_revenus():
    st.header("11. Films avec note > 80 et revenu > 50M")
    result = creer_vue_films_notes_revenus()
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Titre", "rating": "Note", "revenue": "Revenu"})
        st.dataframe(df)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x="Titre", y="Note", ax=ax)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.warning("Aucun film trouvé")

def display_correlation_runtime_revenue():
    st.header("12. Corrélation entre durée et revenu")
    result = correlation_runtime_revenue()
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Film", "runtime": "Durée", "revenue": "Revenu"})
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x="Durée", y="Revenu", ax=ax)
        plt.title("Corrélation entre durée et revenu")
        st.pyplot(fig)
    else:
        st.warning("Aucune donnée disponible")

def display_evolution_duree_par_decennie():
    st.header("13. Évolution de la durée moyenne des films par décennie")
    result = evolution_duree_par_decennie()
    if result:
        df = pd.DataFrame(result).rename(columns={"_id": "Décennie", "avg_runtime": "Durée moyenne"})
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x="Décennie", y="Durée moyenne", ax=ax)
        plt.title("Évolution de la durée moyenne des films par décennie")
        st.pyplot(fig)
    else:
        st.warning("Aucune donnée disponible")
        

# Menu principal
st.sidebar.title("Navigation")
options = [
    "1. Année record de sorties",
    "2. Films post-1999",
    "3. Moyenne votes 2007",
    "4. Films par année",
    "5. Genres disponibles",
    "6. Film le plus rentable",
    "7. Réalisateurs prolifiques",
    "8. Genre le plus rentable",
    "9. Top 3 par décennie",
    "10. Films les plus longs",
    "11. Films bien notés",
    "12. Corrélation durée-revenu",
    "13. Évolution durée moyenne"
]
choice = st.sidebar.selectbox("Choisissez une analyse", options)

# Router vers la fonction d'affichage correspondante
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
else:
    st.warning("Sélectionnez une option valide")

# Footer
st.divider()
st.caption("Application développée avec Streamlit • Données provenant de MongoDB Atlas")