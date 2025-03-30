# Projet NoSQL - ESIEA 2024-2025

## ✨ Objectif
Le but de ce projet est de manipuler deux bases NoSQL (→ MongoDB et Neo4j) pour analyser un corpus de films, d'acteurs et de réalisateurs, et en extraire des informations complexes via des requêtes.

---

## 📁 Structure de la base MongoDB
- **Base :** `entertainment`
- **Collection :** `films`
- **Source :** Fichier `movies.json`
- **Champs principaux :**
  - `_id` : identifiant du film
  - `title`, `year`, `Director`, `Actors`, `genre`, `votes`, `revenue`, `rating`

---

## 🧵 Structure de la base Neo4j
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

## 🤖 Membres ajoutés au graphe
- `Eya BOUALLAGUI`
- `Coralie TADJIFOUE`

Liées au film : **Avatar**

---

## 🔢 Requêtes Cypher (14 à 26)

### 14. Acteur ayant joué dans le plus de films
**Réponse :** Matthew McConaughey (4 films)

### 15. Acteurs ayant joué avec Anne Hathaway
**Réponse :** Matthew McConaughey, Jessica Chastain, etc.

### 16. Acteur avec les plus gros revenus cumulés
**Réponse :** Amy Adams (0)
> Champ `revenue` souvent manquant ou nul dans les données.

### 17. Moyenne des votes
**Réponse :** `None`
> Champ `votes` très peu présent.

### 18. Genre le plus présent
**Réponse :** Drama (49 films)

### 19. Films où ont joué les co-acteurs du groupe projet
**Réponse :** Guardians of the Galaxy, Star Trek Beyond, etc.

### 20. Réalisateur avec le plus d'acteurs différents
**Réponse :** Christopher Nolan (14 acteurs)

### 21. Films les plus connectés (acteurs en commun)
**Réponse :** Captain America / The Avengers, etc.

### 22. Acteurs avec le plus de réalisateurs
**Réponse :** Scarlett Johansson, Ben Affleck, Chris Pratt...

### 23. Recommandation de film pour Anne Hathaway (par genre)
**Réponse :** Rogue One, Guardians of the Galaxy, etc.

### 24. Relations INFLUENCE_PAR entre réalisateurs
**Réponse :** Relations créées via genres communs

### 25. Chemin le plus court entre Tom Hanks et Scarlett Johansson
**Réponse :** Passant par Aaron Eckhart, Christian Bale

### 26. Communautés d'acteurs (Louvain)
**Réponse :** Requête fonctionnelle avec le plugin GDS activé dans Neo4j Desktop

---

## 🎓 Conclusion
Le projet NoSQL a permis d'explorer de manière approfondie les forces de MongoDB (souplesse documentaire) et de Neo4j (exploration de graphe). Les requêtes ont permis d'extraire des données pertinentes, de créer des relations complexes, et d'utiliser des algorithmes d'analyse avancée (Louvain).

---

**Fichier export CSV et visuel seront fournis en complément.**