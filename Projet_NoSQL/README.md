
## Lien Github du projet: https://github.com/BouallaguiEya/projet-NoSQL.git

## Structure de la base MongoDB
- **Base :** `entertainment`
- **Collection :** `films`
- **Source :** Fichier `movies.json`
- **Champs principaux :**
  - `_id` : identifiant du film
  - `title`, `year`, `Director`, `Actors`, `genre`, `votes`, `revenue`, `rating`

---

## Structure de la base Neo4j
- **Nœuds :**
  - `Film(id, title, year, rating, revenue, votes)`
  - `Acteur(name)`
  - `Realisateur(name)`
  - `Genre(name)`

- **Relations :**
  - `(:Acteur)-[:A_JOUE]->(:Film)`
  - `(:Realisateur)-[:A_REALISE]->(:Film)`
  - `(:Film)-[:GENRE]->(:Genre)`
  - `(:Realisateur)-[:INFLUENCE_PAR]->(:Realisateur)`

- **Importation depuis MongoDB faite via Python (pymongo + neo4j)**

---

## Membres ajoutés au graphe
- `Eya BOUALLAGUI`
- `Coralie TADJIFOUE`

Liées au film : **Avatar**

---

## Pour lancer l'application: (python -m) streamlit run app.py