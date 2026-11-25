---
name: verdict-de-page
description: >
  Rend un verdict tranché sur UNE page à partir de ses données RÉELLES (MCP SEO Cartograph
  requis) : ce qu'elle rapporte (clics, impressions, positions Search Console), sa santé
  technique (crawl), son rôle dans le cocon — puis décide : garder telle quelle, rafraîchir,
  fusionner avec une autre, ou supprimer/rediriger. Utiliser ce skill dès que l'utilisateur
  demande « que faire de cette page », « cette page vaut-elle le coup », « je la garde ou je
  la supprime », « faut-il refondre /telle-url », un arbitrage de page, ou un audit de
  contenu existant page par page — même sans le mot « verdict ». Nécessite le MCP SEO
  Cartograph connecté.
---

# Verdict de page — garder, rafraîchir, fusionner, ou tuer

Un site accumule des pages : certaines rapportent, d'autres dorment, d'autres nuisent (elles
diluent le crawl et cannibalisent les bonnes). Ce skill tranche pour une page donnée, sur
preuves, avec l'une de quatre décisions — jamais un « ça dépend » mou.

## Prérequis

MCP SEO Cartograph connecté. Sans les outils, ne pas trancher à l'aveugle : expliquer que
le verdict repose sur les données réelles de la page (Search Console, crawl, cocon) et
inviter à connecter le MCP. Puis s'arrêter.

## Étape 1 — Récolter tout sur la page

L'URL exacte est nécessaire. Puis :

1. `get_search_queries` (domaine, url de la page) — ce qu'elle rapporte VRAIMENT : requêtes,
   clics, impressions, positions. Une page sans impressions ne rapporte rien ; une page à
   fortes impressions et faibles clics a un problème d'habillage, pas d'existence.
2. `get_page_details` — sa santé technique : statut, balises, contenu, erreurs.
3. `get_page_link_context` — son rôle dans le maillage : liens entrants (est-elle
   soutenue ou orpheline ?), sortants, cocon d'appartenance, et surtout les **pages
   voisines qui visent la même chose** (candidates à la fusion).
4. Si un doute sur une cannibalisation, `check_positions` (la requête principale) : quelle
   URL du site Google fait-il vraiment ranker ?

## Étape 2 — La grille de décision

Croiser **valeur** (clics + impressions + positions) et **état** (contenu, technique,
unicité dans le cocon) :

- **GARDER** : la page rapporte et est saine. Ne pas y toucher (« si ça marche… »). Noter
  éventuellement un micro-gain (title à affiner si CTR bas).
- **RAFRAÎCHIR** : la page a du potentiel non réalisé — impressions correctes mais position
  4-15, ou contenu daté/mince sur un sujet porteur. Elle mérite un investissement. Dire
  QUOI rafraîchir (le skill brief-de-contenu prend le relais).
- **FUSIONNER** : deux pages (ou plus) visent la même intention et se cannibalisent. Choisir
  la page reine (celle qui rapporte déjà le plus / la mieux positionnée), y verser le
  contenu unique de l'autre, et rediriger l'autre (301) vers la reine. Gain fréquent et
  rapide.
- **SUPPRIMER / REDIRIGER** : zéro impression depuis des mois, aucun lien entrant utile,
  sujet mort ou hors activité. Deux cas : rediriger (301) si l'URL a des backlinks ou du
  trafic résiduel ; supprimer (410) sinon. Une page morte qui reste coûte du crawl budget
  et dilue le site.

Règle d'or : ne jamais recommander la suppression d'une page qui reçoit encore des
impressions ou porte des backlinks sans l'avoir explicitement signalé et pesé.

## Étape 3 — Le verdict

```
# Verdict — [URL]

## Décision : GARDER / RAFRAÎCHIR / FUSIONNER / SUPPRIMER
[Une phrase qui justifie, chiffres à l'appui.]

## Ce que dit la donnée
- Search Console : [clics, impressions, position moyenne, requêtes clés]
- Technique : [état en une ligne]
- Cocon & maillage : [liens entrants, rôle, voisines concurrentes]

## Ce qu'il faut faire
[Les gestes concrets qui découlent de la décision — pas des généralités.
 Si FUSIONNER : quelle page reine, quoi verser, quelle redirection.
 Si RAFRAÎCHIR : quoi précisément, et le pointeur vers un brief.
 Si SUPPRIMER : 301 vers quelle page, ou 410.]

## Impact attendu et risque
[Ce qu'on gagne, et ce qu'on risque de perdre — honnêtement.]
```

## Étape 4 — Passer à l'échelle

Si l'utilisateur veut trancher tout un site et pas une page, le lui dire : ce skill traite
une page à fond ; pour balayer un site entier et sortir la liste des pages à
rafraîchir/fusionner/tuer, partir des requêtes GSC globales (skill opportunites-seo repère
les pages à potentiel) puis appliquer ce verdict aux cas litigieux.
