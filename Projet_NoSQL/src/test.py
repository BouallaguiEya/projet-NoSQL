import streamlit as st
import pandas as pd
from mongo_queries import *

def main():
    st.set_page_config(page_title="Analyse des films", layout="wide")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Aller à", [
        "Année avec le plus grand nombre de films",
        "Nombre de films après 1999",
        "Moyenne des votes des films en 2007",
        "Nombre de films par année",
        "Genres de films disponibles",
        "Film ayant généré le plus de revenus",
        "Réalisateurs avec plus de 5 films",
        "Genre avec le plus haut revenu moyen",
        "Top 3 films par décennie",
        "Film le plus long par genre",
        "Vue MongoDB : Films bien notés et rentables",
        "Corrélation entre durée et revenu",
        "Évolution de la durée des films par décennie"
    ])
    
    if page == "Année avec le plus grand nombre de films":
        result = ann_plus_grand_nbr_films()
        if result:
            st.write(f"L'année avec le plus de films est **{result['_id']}** avec {result['count']} films.")
        else:
            st.write("Aucune donnée trouvée.")

    elif page == "Nombre de films après 1999":
        count = films_apres_1999()
        st.write(f"Nombre de films après 1999 : **{count}**")

    elif page == "Moyenne des votes des films en 2007":
        try:
            avg_votes = moy_votes_2007()
            st.write(f"Moyenne des votes des films sortis en 2007 : **{avg_votes:.2f}**")
        except:
            st.write("Aucune donnée disponible.")
    
    elif page == "Nombre de films par année":
        data = nbr_films_par_annee()
        df = pd.DataFrame(data)
        df.rename(columns={"_id": "Année", "count": "Nombre de films"}, inplace=True)
        st.bar_chart(df.set_index("Année"))
    
    elif page == "Genres de films disponibles":
        genres = genre_films_dispo()
        st.write("Genres disponibles :", ", ".join(genres))
    
    elif page == "Film ayant généré le plus de revenus":
        film = film_plus_revenu()
        if film:
            st.write(f"Le film avec le plus de revenus est **{film['title']}** avec **${film['revenue']:,}**")
    
    elif page == "Réalisateurs avec plus de 5 films":
        data = realisateurs_plus_5_films()
        df = pd.DataFrame(data)
        df.rename(columns={"_id": "Réalisateur", "count": "Nombre de films"}, inplace=True)
        st.write(df)
    
    elif page == "Genre avec le plus haut revenu moyen":
        data = genre_plus_revenu_moyen()
        if data:
            genre = data[0]
            st.write(f"Le genre le plus rentable en moyenne est **{genre['_id']}** avec un revenu moyen de **${genre['revenu_moyen']:,}**")
    
    elif page == "Top 3 films par décennie":
        data = top_3_films_par_decennie()
        for entry in data:
            st.write(f"**Décennie {entry['_id']}**")
            for film in entry['top3']:
                st.write(f"- {film['title']} (Note: {film['rating']})")
    
    elif page == "Film le plus long par genre":
        data = film_plus_long_par_genre()
        df = pd.DataFrame(data)
        df.rename(columns={"_id": "Genre", "film": "Film", "runtime": "Durée (min)"}, inplace=True)
        st.write(df)
    
    elif page == "Vue MongoDB : Films bien notés et rentables":
        data = creer_vue_films_notes_revenus()
        df = pd.DataFrame(data)
        st.write(df)
    
    elif page == "Corrélation entre durée et revenu":
        correlation = correlation_runtime_revenue()
        st.write(correlation)
    
    elif page == "Évolution de la durée des films par décennie":
        data = evolution_duree_par_decennie()
        df = pd.DataFrame(data)
        df.rename(columns={"_id": "Décennie", "duree_moyenne": "Durée moyenne"}, inplace=True)
        st.line_chart(df.set_index("Décennie"))

if __name__ == "__main__":
    main()
