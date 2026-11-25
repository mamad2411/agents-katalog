---
name: chantier-maillage
description: >
  Mène un chantier de maillage interne complet sur les données réelles du site (MCP SEO
  Cartograph requis) : lit la carte des cocons et le link map, identifie les pages à
  renforcer (orphelines, faibles en liens, positions 4-15 à pousser), propose des liens
  internes justifiés avec ancre et emplacement, et les envoie dans le cockpit pour
  validation humaine. Utiliser ce skill dès que l'utilisateur parle de maillage interne,
  liens internes, cocons, pages orphelines, « renforcer une page », « pousser une page
  qui stagne », ou veut améliorer la structure de son site — même sans le mot
  « maillage ». Nécessite le MCP SEO Cartograph connecté (app.tnedjar.com).
---

# Chantier de maillage interne — renforcer ce qui peut gagner

Le maillage interne est le levier SEO le moins cher : pas de contenu à produire, pas de
lien à acheter — juste dire à Google quelles pages comptent. Mais un lien interne sans
justification est du bruit. Chaque proposition de ce chantier doit répondre à : *pourquoi
cette page mérite-t-elle ce lien, et pourquoi depuis cette page source ?*

## Prérequis

MCP SEO Cartograph connecté, avec au moins un crawl remonté. Sans les outils
(`get_link_map`, `get_clusters_data`…), ne pas improviser : expliquer que le chantier se
fait sur le maillage réel crawlé et inviter à connecter le MCP (app.tnedjar.com), puis
s'arrêter.

## Étape 1 — La cible (ne pas mailler dans le vide)

Demander (ou déduire) l'objectif du chantier — il détermine tout le reste :
- **Pousser des pages précises** (elles stagnent en position 4-15) → vérifier leurs
  positions réelles : `get_search_queries` (les requêtes où elles apparaissent) et/ou
  `get_tracked_positions`. Les pages en position 4-10 sont les cibles à meilleur retour.
- **Assainir la structure** → chercher les orphelines et les pages profondes.
- **Renforcer un cocon** entier (nouveau contenu, cluster stratégique) → partir du cluster.

## Étape 2 — Lire le terrain

1. `get_clusters_data` — la carte des cocons : quel cluster porte la cible, lesquels
   sont adjacents (les liens intra-cocon d'abord, inter-cocons seulement si sémantiquement
   justifiés).
2. `get_link_map` — le maillage réel : qui pointe déjà vers la cible, avec quelles
   ancres ; les pages fortes du site (beaucoup de liens entrants) qui pourraient donner.
3. `get_page_link_context` sur chaque page cible — son contexte exact : liens entrants,
   sortants, ancres utilisées, voisins de cluster.
4. `update_link_exclusions` n'est PAS à toucher sans demande explicite de l'utilisateur.

## Étape 3 — Proposer (les règles du lien qui compte)

- **La source donne, la cible reçoit** : chercher des sources à la fois fortes (liens
  entrants) et proches sémantiquement (même cluster ou cluster adjacent). Un lien depuis
  une page hors-sujet, même forte, vaut peu.
- **L'ancre décrit la cible, pas la source** — et varie : jamais deux fois la même ancre
  exacte depuis deux sources ; utiliser les formulations réelles des requêtes GSC
  (`get_search_queries` sur la page cible) comme vivier d'ancres naturelles.
- **L'emplacement compte** : un lien dans le corps du texte, entouré de contexte, bat un
  lien de fin de page. Chaque proposition précise OÙ insérer (après quel passage) et
  fournit la phrase d'insertion complète.
- **3 à 5 liens par page cible** suffisent pour un chantier ; au-delà, on dilue.
- Ne jamais proposer un lien qui existe déjà (vérifier dans le link map).

## Étape 4 — Envoyer au cockpit, pas appliquer

Chaque lien retenu part via `propose_internal_link` : source, cible, ancre, justification
courte (position actuelle + requête visée + force de la source). Les propositions
atterrissent dans le Netlinker du cockpit où l'utilisateur les valide — l'application sur
le site réel reste humaine. Le dire clairement en fin de chantier : « X propositions
envoyées dans ton Netlinker, à valider sur app.tnedjar.com ».

## Étape 5 — Restituer et mesurer

Terminer par un récapitulatif : tableau des propositions (source → cible, ancre,
justification), et la mesure : si les pages cibles ne sont pas dans le rank tracker, les
y mettre (`track_keywords` avec leurs requêtes principales) — le prochain
`get_tracked_positions` dira si le chantier a payé. Donner l'horizon honnête : un lien
interne produit son effet en 2 à 6 semaines.
