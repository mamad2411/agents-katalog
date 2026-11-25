---
name: audit-technique
description: >
  Produit un audit SEO technique complet à partir du crawl RÉEL du site (MCP SEO Cartograph
  requis) : erreurs par typologie (systémiques vs isolées), profondeur, statuts HTTP, balises
  manquantes ou dupliquées, maillage cassé, indexabilité — priorisé par impact et livré en
  rapport lisible. Utiliser ce skill dès que l'utilisateur demande un audit technique, un
  audit SEO, « qu'est-ce qui cloche techniquement sur mon site », « check les erreurs », un
  diagnostic de site, ou veut la liste priorisée des corrections techniques — même sans le
  mot « audit ». Nécessite le MCP SEO Cartograph connecté avec un crawl remonté ; sans crawl,
  proposer de le lancer (request_crawl) plutôt qu'auditer à l'aveugle.
---

# Audit technique — le crawl dit tout, encore faut-il le lire

Un audit technique n'est pas une liste d'erreurs : c'est un tri. Cent pages avec le même
title dupliqué, ce n'est pas cent problèmes — c'est UN problème de template à corriger une
fois. La valeur de l'audit est dans la distinction **systémique** (le gabarit, la config —
une correction touche des centaines de pages) vs **isolé** (une page précise). Toujours
regrouper avant de lister.

## Prérequis

MCP SEO Cartograph connecté avec au moins un crawl remonté. Sans crawl disponible
(`list_crawl_sites` vide), ne pas improviser depuis l'extérieur : proposer de lancer un
crawl (`request_crawl`) et expliquer que l'audit technique se fait sur le crawl complet,
pas sur quelques pages vues du dehors. Puis s'arrêter.

## Étape 1 — Cadrer le crawl

1. `list_crawl_sites` (confirmer le site) puis `list_crawls_for_site` — prendre le dernier
   crawl, et noter s'il en existe un précédent (comparer deux crawls révèle ce qui s'est
   dégradé ou amélioré depuis le dernier passage — un audit qui montre une tendance vaut
   plus qu'une photo).
2. `get_crawl_overview` — la vue d'ensemble : nombre de pages, statuts, l'ampleur des
   grands postes d'erreur. C'est la carte avant le détail.

## Étape 2 — Récolter par typologie

`get_crawl_data` section par section, dans l'ordre de gravité SEO :

1. **`siteinfo` + `crawl_audit`** : la santé globale et les issues agrégées par type —
   c'est ici qu'on repère le systémique (un type d'erreur qui touche un gros pourcentage
   des pages = template/config).
2. **`broken_links`** : liens internes cassés (404) — mauvais pour l'utilisateur ET le
   crawl budget. Séparer les liens cassés *dans* le contenu (à corriger) des liens vers
   des pages supprimées (à rediriger).
3. **`issues`** : le détail — titles/meta manquants ou dupliqués, H1 absents/multiples,
   images sans alt, contenu trop court, canonical incohérents, profondeur excessive.
4. **`maillage`** : pages orphelines (aucun lien entrant = invisibles pour Google), pages
   trop profondes (> 3-4 clics de la home = mal crawlées).
5. **`sitemap`** : écarts sitemap ↔ crawl (pages au sitemap introuvables au crawl, pages
   crawlées absentes du sitemap).

Pour les pages critiques ou les cas ambigus, `get_page_details` (une page précise) et
`inspect_url` (statut d'indexation Google réel) confirment avant d'affirmer.

## Étape 3 — Diagnostiquer et prioriser

Classer chaque constat sur deux axes :

- **Portée** : systémique (template/config) ou isolé (N pages nommées).
- **Impact SEO** : bloquant (empêche l'indexation ou le crawl — noindex accidentel, chaînes
  de redirections, 404 massifs, pages orphelines stratégiques) / frein (title dupliqué,
  H1 manquant, contenu maigre) / cosmétique (alt manquants sur images décoratives).

La règle de priorisation : **systémique + bloquant** d'abord (une correction, énorme
effet), puis systémique + frein, puis isolé + bloquant, et on ne noie pas le rapport avec
le cosmétique (le mentionner en bloc, pas en liste).

## Étape 4 — Le rapport

```
# Audit technique SEO — [domaine] — [date du crawl]

## Verdict (3 phrases)
[État général, le problème dominant, la priorité n°1.]

## Chiffres clés
| Pages crawlées | Erreurs bloquantes | Freins | Pages orphelines | Liens cassés |
[+ tendance vs crawl précédent si disponible : ↑ / ↓ / stable]

## À corriger en priorité (systémique)
Pour chaque poste : le problème, COMBIEN de pages, la cause probable (souvent le template),
l'action concrète, l'effort. Une correction ici vaut cent corrections page par page.

## À corriger ensuite (isolé)
Les pages précises nommées, groupées par type de correction.

## Points sains
Ce qui va bien — un audit qui n'a que du rouge n'est pas crédible.

## Cosmétique (bloc, non détaillé)
[Le reste, en une ligne : « X images sans alt, à traiter au fil de l'eau. »]
```

En français par défaut, en anglais si demandé. Niveau adapté : client final = chaque terme
technique expliqué en une incise ; développeur/consultant = dense, on garde le jargon.

## Étape 5 — La suite

Si des corrections on-page se dégagent (title, meta, H1 sur des pages précises), proposer
de les envoyer dans l'Éditeur du cockpit (`send_issues_to_editor` puis `propose_fix_value`)
pour que l'utilisateur les valide et applique. Si le maillage ressort comme problème
dominant, passer le relais au skill chantier-maillage. Si c'est le contenu maigre,
au skill brief-de-contenu.
