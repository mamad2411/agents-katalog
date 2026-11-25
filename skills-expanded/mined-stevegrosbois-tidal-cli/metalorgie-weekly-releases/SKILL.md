---
name: metalorgie-weekly-releases
description: >
  Récupère et filtre les sorties d'albums de la semaine publiées sur metalorgie.com ("Les sorties de la semaine").
  Affiche les albums correspondant aux genres favoris de l'utilisateur (Metalcore, Post Hardcore, Hardcore, Neo metal)
  ainsi que les albums de groupes reconnus/notables, même hors genres favoris.
  Utilise ce skill dès que l'utilisateur mentionne metalorgie, les sorties de la semaine, les nouvelles sorties metal,
  les albums du vendredi, ou veut savoir quoi écouter de nouveau cette semaine.
---

# Sorties de la semaine — Metalorgie

## Objectif

Aller chercher le dernier article "Les sorties de la semaine" sur metalorgie.com, puis filtrer et présenter les sorties pertinentes pour l'utilisateur.

## Genres favoris de l'utilisateur

Vérifier dans CLAUDE.local.md ou demander à l'utilisateur puis les sauvegarder dans CLAUDE.local.md.

## Étapes

### 1. Trouver l'article de la semaine

Fetche la page d'accueil de metalorgie.com et repère le lien vers le dernier article "Les sorties de la semaine" (il est publié chaque vendredi). L'URL suit ce pattern : `https://www.metalorgie.com/news/<id>-les-sorties-de-la-semaine-<slug>`.

Si l'utilisateur a précisé un numéro de semaine ou une date, cherche l'article correspondant.

### 2. Récupérer le contenu de l'article

Fetche l'article trouvé. Le contenu liste les sorties sous forme :
```
- [Groupe] - Titre Album (Genre, Pays) 🎧
```
Les genres apparaissent entre parenthèses, parfois multiples séparés par `/`.

### 3. Filtrer et classer les sorties

Construis **deux listes** :

**Liste A — Genres favoris**
Inclus toute sortie dont le genre correspond (même partiellement) à : Metalcore, Post Hardcore, Hardcore, Neo metal. Applique une correspondance souple : "Hardcore Mélodique", "Melodic Metalcore", "Deathcore", "Mathcore" peuvent être inclus si pertinents.

**Liste B — Groupes notables**
Indépendamment du genre, inclus les sorties de groupes largement reconnus dans la sphère metal mondiale (groupes signés sur grands labels, avec une large base de fans, régulièrement en tournée dans les grandes salles). Utilise ta connaissance des groupes pour juger. Si un groupe apparaît déjà dans la Liste A, ne le duplique pas.

### 4. Présenter les résultats

Formate la réponse ainsi :

```
## Sorties de la semaine [numéro] — [date]

### Tes genres (Metalcore / Post Hardcore / Hardcore / Neo metal)
| Groupe | Album | Genre |
|--------|-------|-------|
| ...    | ...   | ...   |

### Groupes notables (autres genres)
| Groupe | Album | Genre |
|--------|-------|-------|
| ...    | ...   | ...   |
```

Si une des deux listes est vide, indique-le brièvement.

## Notes

- Si l'article n'est pas encore paru (ex. demande en cours de semaine), indique la date du prochain vendredi.
- Ne liste pas les EPs ou singles sauf si l'utilisateur le demande explicitement.
- Le nombre de semaine dans le titre de l'article correspond au numéro de semaine ISO de l'année.
