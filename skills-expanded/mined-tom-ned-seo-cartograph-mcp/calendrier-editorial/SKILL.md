---
name: calendrier-editorial
description: >
  Construit un calendrier éditorial SEO — quoi publier, dans quel ordre et à quelle date —
  à partir des données RÉELLES du compte SEO Cartograph (MCP requis) : opportunités
  (positions 4-20 à pousser), trous de contenu dans les cocons, saisonnalité du trafic
  Search Console, et clusters à compléter. Chaque entrée sort avec sa requête cible, son
  type, sa priorité, sa fenêtre de publication et son maillage. Utiliser ce skill dès que
  l'utilisateur demande un calendrier éditorial, un planning de contenu, un plan de
  publication, « qu'est-ce que je publie et quand », « organise ma production de contenu
  sur 3 mois », « content calendar SEO » — même sans le mot « calendrier ». Nécessite le MCP
  SEO Cartograph connecté. (Pour planifier des posts réseaux sociaux, c'est le calendrier
  de publication d'ED, pas ce skill.)
---

# Calendrier éditorial — publier au bon moment ce qui rapportera

Un calendrier éditorial SEO n'est pas une liste de sujets étalée sur des dates au hasard.
C'est un **ordre de bataille** : commencer par ce qui rapporte vite (momentum), construire
les cocons dans le bon sens (le pilier avant ses satellites), et publier AVANT le pic de
demande, pas pendant. Toute la valeur est dans la priorisation et le timing — deux choses
que seules les données réelles permettent.

## Prérequis

MCP SEO Cartograph connecté (Search Console + crawl). Sans les outils (`get_search_queries`,
`get_clusters_data`, `get_analytics_history`…), ne pas improviser un planning générique :
expliquer que le calendrier se construit sur la demande réelle et les cocons du site, et
inviter à connecter le MCP. Puis s'arrêter.

## Étape 1 — Cadrer

Verrouiller avec l'utilisateur : l'**horizon** (4 semaines, 1 trimestre, 6 mois) ; la
**cadence réaliste** (combien de contenus par semaine/mois — un calendrier qu'on ne tiendra
pas ne sert à rien) ; l'**objectif dominant** (gagner du trafic vite, couvrir un cocon en
profondeur, préparer une saison) ; le marché (locale). Confirmer le domaine.

## Étape 2 — Rassembler la matière

1. `get_search_queries` (domaine, limit élevée) — la demande réelle : requêtes, volumes
   relatifs (impressions), positions. C'est le vivier de sujets ET la mesure de ce qui
   vaut la peine.
2. `get_clusters_data` — les cocons : lesquels sont bien couverts, lesquels ont des
   **trous** (thématique amorcée mais incomplète = terrain le plus fertile). Un cluster à
   moitié construit rend chaque nouvel article plus efficace que dix articles isolés.
3. `get_analytics_history` (domaine, mensuel + quotidien) — la **saisonnalité** : quand le
   trafic du site monte et descend. Croiser avec le calendrier réel (un fleuriste publie
   sur la Saint-Valentin en décembre, pas en février). C'est ce qui détermine les DATES.
4. `get_link_map` — les pages fortes existantes, futures sources de liens vers les nouveaux
   contenus, et la structure des cocons à renforcer.
5. Optionnel, sur 3-5 sujets prioritaires seulement (coûte des crédits) : `get_serp` pour
   confirmer que la première page est prenable et relever le format qui gagne.

## Étape 3 — Prioriser et séquencer (le cœur du skill)

Attribuer à chaque sujet candidat un **score de priorité** (potentiel × facilité) et une
**place dans la séquence** :

- **Retour rapide d'abord** : les sujets où une page existe déjà en position 4-15 (un
  rafraîchissement/renfort suffit) passent avant les créations from scratch — ils
  ramènent du trafic vite et créent l'élan.
- **Cocon dans le bon ordre** : au sein d'un cluster à compléter, la page pilier
  (transactionnelle, large) avant ses satellites (longue traîne) — les satellites la
  renforcent, pas l'inverse. Grouper les articles d'un même cocon sur une même période
  pour un effet de masse.
- **Timing saisonnier** : reculer la date de publication de 4 à 8 semaines AVANT le pic de
  demande observé — Google a besoin de temps pour indexer et faire monter la page. Publier
  le contenu de Noël en octobre.
- **Cadence tenable** : ne remplir le calendrier que jusqu'à la capacité déclarée. Mieux
  vaut 2 articles/mois tenus que 8 promis et 3 livrés.

## Étape 4 — Le calendrier

```
# Calendrier éditorial SEO — [domaine] — [horizon]
Cadence : [N contenus / période] · Objectif : […]

## Vue d'ensemble
[2-3 phrases : la logique du plan — par quoi on commence et pourquoi, les temps forts
saisonniers, l'ordre des cocons.]

## Le calendrier
| Semaine/Mois | Sujet / requête cible | Type | Cluster | Priorité | Action | Maillage |
|---|---|---|---|---|---|---|
[Chaque ligne :
 - Sujet + requête cible réelle (formulation issue de la GSC)
 - Type : nouvel article / refonte / page service / pilier / satellite
 - Cluster d'appartenance
 - Priorité : 🔥 retour rapide / ⭐ stratégique / 🌱 fond
 - Action concrète : « créer », « refondre /url », « enrichir »
 - Liens internes à poser à la publication : depuis quelles pages, vers quelles pages]

## Temps forts saisonniers
[Les pics de demande repérés et les contenus calés en amont, avec la date de publication
conseillée — pas la date de l'événement.]

## Pour bien démarrer
[Les 2-3 premières entrées expliquées : pourquoi elles ouvrent le calendrier.]
```

En français par défaut, en anglais si le marché l'exige.

## Étape 5 — Alimenter la production

Chaque ligne du calendrier est une entrée directe pour le skill **brief-de-contenu** (qui
transforme un sujet en brief rédacteur complet) ou **landing-page-seo** (pour une page de
conversion). Le proposer. Et proposer de mettre les requêtes cibles du calendrier sous
surveillance (`track_keywords`) pour mesurer, mois après mois, si le plan éditorial produit
ses effets — le calendrier devient alors pilotable, pas juste un document figé.
