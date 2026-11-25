---
name: brief-de-contenu
description: >
  Rédige un brief de contenu prêt pour un rédacteur, calibré sur les données RÉELLES du
  compte SEO Cartograph (MCP requis) : requête cible et champ lexical issus de la Search
  Console, structure déduite de la SERP (titles gagnants, PAA, recherches associées),
  angle différenciant vs le top 10, longueur cible, questions à couvrir, et plan de
  maillage interne. Utiliser ce skill dès que l'utilisateur veut un brief, un plan
  d'article, « prépare le contenu pour le rédacteur », « sur quoi et comment écrire pour
  ranker sur [requête] », « brief SEO » — même sans le mot « brief ». Nécessite le MCP SEO
  Cartograph connecté (Search Console et crawl).
---

# Brief de contenu — écrire pour la requête, pas pour soi

Un rédacteur a besoin de trois choses qu'un brief médiocre ne donne jamais : sur quoi
Google juge cette requête (le format qui gagne), quel angle prendre pour ne pas répéter le
top 10, et exactement quoi couvrir. Ce brief les fournit à partir des vraies données, pas
d'intuitions.

## Prérequis

MCP SEO Cartograph connecté. Sans les outils (`get_search_queries`, `get_serp`…), ne pas
improviser un brief générique : expliquer qu'il se construit sur la Search Console réelle
et la SERP live, et inviter à connecter le MCP. Puis s'arrêter.

## Étape 1 — Cadrer

Verrouiller avec l'utilisateur : la **requête cible** (une seule) et le marché (locale,
défaut `fr-ch`) ; l'**intention de la page** (informer, convertir, comparer) ; s'il s'agit
d'un **nouvel article** ou de la **refonte** d'une page existante (si refonte, récupérer
son URL — on partira de ses requêtes actuelles). Vérifier le solde SERP (`get_serp_credits`,
~2-4 crédits pour un brief).

## Étape 2 — La donnée

1. `get_search_queries` (domaine ; et l'URL si refonte) — le champ lexical RÉEL : les
   formulations exactes des internautes, les requêtes voisines, les positions actuelles.
   C'est le vocabulaire à couvrir, pas celui qu'on imagine.
2. `get_serp` (requête cible) — le top 10 : relever le **type de page qui gagne** (guide,
   comparatif, page service, fiche), les **angles des titles** (prix, délai, « meilleur »,
   localité), les **PAA** (→ sections/FAQ obligatoires) et les **recherches associées**
   (→ sous-thèmes à couvrir).
3. `get_clusters_data` — dans quel cocon l'article s'insère : les pages sœurs qui devront
   le lier et celles qu'il devra pointer.
4. `get_link_map` — les pages fortes du site, sources de liens internes vers le futur
   article.

## Étape 3 — Décider l'angle

La SERP montre ce qui existe déjà. Le brief doit dire comment être meilleur ou différent :
plus complet, plus à jour, plus local, plus concret (données, exemples), meilleur format
(le top 5 est en pavés indigestes → structurer ; le top 5 est mince → approfondir). Ne
jamais briefer « comme le n°1 » — briefer « ce que le n°1 ne fait pas ».

## Étape 4 — Le brief

```
# Brief de contenu — « [requête cible] »

## En bref
- Requête cible : … | Intention : … | Marché : …
- Type de page attendu (d'après la SERP) : …
- Angle différenciant : [la phrase qui dit pourquoi cette page méritera le clic]
- Longueur indicative : … mots (calibrée sur le top 10, pas un chiffre magique)

## Titre et meta (propositions, pas contraintes)
- Title (≤ 60) : …
- H1 : … (différent du title)
- Meta description (≤ 155) : …
- Slug : …

## Plan détaillé (H2 / H3)
Pour chaque section : l'intitulé, ce qu'elle doit couvrir, et les mots/expressions réels
(issus de la Search Console) à y intégrer NATURELLEMENT — jamais de bourrage.

## Questions à répondre (issues des PAA)
[Liste — elles nourrissent le corps ET une éventuelle FAQ + schema FAQPage.]

## À NE PAS oublier
- Preuves/exemples/données concrètes à demander au client
- Éléments E-E-A-T : qui signe, sur quelle expertise
- Call-to-action attendu

## Maillage interne
- Liens ENTRANTS à créer : [3-5 pages existantes → ancre exacte à utiliser]
- Liens SORTANTS de l'article : [2-3 pages sœurs du cocon]

## Consignes de forme
Ton, personne (vous/tu), niveau de technicité, ce qu'il faut éviter.
```

En français par défaut, en anglais si le marché l'exige. Le champ lexical et les PAA
restent dans la langue de la SERP interrogée.

## Étape 5 — La suite

Proposer de mettre la requête cible sous surveillance dès maintenant (`track_keywords`)
pour mesurer l'effet de l'article une fois publié. Si l'utilisateur veut la page complète
et pas seulement le brief, enchaîner avec le skill landing-page-seo (pour une page de
conversion) — le brief lui sert directement d'entrée.
