---
name: opportunites-seo
description: >
  Détecte les opportunités SEO à meilleur retour sur effort à partir des données réelles
  du compte SEO Cartograph (MCP requis) : quick wins positions 4-10 (un coup de pouce pour
  le top 3), positions 11-20 (page 2 → page 1), pages qui impriment sans cliquer (title/
  meta à retravailler), cannibalisations, et requêtes où le site est absent mais légitime.
  Chaque opportunité sort avec son action concrète et son effort estimé. Utiliser ce skill
  dès que l'utilisateur demande « quoi faire en priorité », « des quick wins », « où est
  le potentiel », « qu'est-ce que j'optimise ce mois-ci », ou cherche des gains rapides —
  même sans le mot « opportunité ». Nécessite le MCP SEO Cartograph connecté
  (app.tnedjar.com).
---

# Opportunités SEO — l'effort au bon endroit

Une opportunité n'est pas « un mot-clé où on pourrait ranker » : c'est un écart entre la
position actuelle et la position accessible, avec un effort borné. Ce skill trie tout le
potentiel du site par retour sur effort, en cinq gisements — du moins cher au plus cher.

## Prérequis

MCP SEO Cartograph connecté avec Search Console branchée. Sans les outils, ne pas
improviser une liste générique : expliquer que la détection travaille sur les requêtes
réelles du site et inviter à connecter le MCP (app.tnedjar.com), puis s'arrêter.

## Étape 1 — Collecter

1. `get_search_queries` (domaine, limit 500+) — la matière première : chaque requête avec
   clics, impressions, CTR et position réelle.
2. `get_tracked_positions` — les mots-clés déjà suivis (cannibalisations signalées).
3. `get_clusters_data` — pour rattacher chaque opportunité à son cocon (une opportunité
   isolée se traite mal ; en grappe, un chantier de maillage la porte).
4. `get_serp_credits` puis, sur les 3-5 requêtes les plus prometteuses seulement,
   `get_serp` — vérifier qui occupe le podium et si la première page est prenable
   (éviter de promettre un top 3 face à trois mastodontes).

## Étape 2 — Les cinq gisements (dans l'ordre du retour sur effort)

1. **Positions 4-10 (quick wins top 3)** : la page ranke déjà — Google la juge légitime.
   Actions types : 2-3 liens internes depuis des pages fortes, enrichissement ciblé
   (répondre à une PAA manquante), title plus incisif. Effort : heures.
2. **CTR anormalement bas** : position ≤ 5 mais CTR < ~3 %, ou impressions massives sans
   clics — le contenu ranke, l'habillage ne vend pas. Action : réécrire title + meta
   (promesse + différenciant), vérifier le rich snippet. Effort : minutes par page.
3. **Positions 11-20 (page 2 → page 1)** : le sujet est validé, la page manque de poids.
   Actions : maillage + contenu complété sur les requêtes voisines (le champ lexical réel
   est dans les requêtes GSC de la page). Effort : demi-journée par page.
4. **Cannibalisations** : deux pages se disputent une requête (visible quand l'URL qui
   ranke n'est pas la cible, ou deux URLs alternent). Action : choisir la page reine,
   rediriger ou différencier l'autre. Effort : faible, gain souvent immédiat.
5. **Absences légitimes** : requêtes du cocon où le site n'apparaît pas (croiser les
   recherches associées de `get_serp` avec les clusters). Action : nouvelle page — c'est
   le gisement le plus cher, ne le proposer que s'il reste du budget effort. (Et pour la
   produire : le skill landing-page-seo.)

## Étape 3 — Restituer

Tableau unique trié par retour sur effort décroissant :

| # | Opportunité | Gisement | Position | Potentiel | Action concrète | Effort |
|---|---|---|---|---|---|---|

Règles de restitution : maximum 10-12 lignes (au-delà, personne n'agit) ; le « potentiel »
en clics estimés/mois (impressions × CTR de la position visée), pas en promesses vagues ;
chaque action est exécutable telle quelle — « réécrire le title de /page : proposer …» et
non « optimiser la page ». Si l'utilisateur a donné un budget temps, ne remplir le tableau
que jusqu'à ce budget.

## Étape 4 — Boucler

Proposer de mettre les requêtes du tableau sous surveillance (`track_keywords`) pour
mesurer, et rappeler que les gisements 1 et 3 se traitent bien en chantier groupé — le
skill chantier-maillage prend le relais.
