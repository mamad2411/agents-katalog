---
name: bilan-seo-mensuel
description: >
  Produit le bilan SEO mensuel complet d'un site à partir des données RÉELLES du compte
  SEO Cartograph (MCP requis) : évolution Search Console et GA4, mouvements de positions
  du rank tracker, répartition top 3/10/20, comparaison des SERP archivées, santé du crawl
  — synthétisés en un rapport lisible par un client final, avec les 3 actions du mois
  prochain. Utiliser ce skill dès que l'utilisateur demande un bilan, un rapport SEO, un
  point mensuel, « où en est mon SEO », « prépare le reporting client », ou veut mesurer
  l'effet d'un chantier — même sans le mot « bilan ». Nécessite le MCP SEO Cartograph
  connecté (app.tnedjar.com) ; sans lui, expliquer comment le connecter plutôt que
  d'improviser un rapport sans données.
---

# Bilan SEO mensuel — les données racontent, le rapport tranche

Un bon bilan répond à trois questions dans l'ordre : *qu'est-ce qui a bougé ?* (les faits),
*pourquoi ?* (le diagnostic), *qu'est-ce qu'on fait ?* (3 actions max). Tout le reste est
du remplissage. Le rapport doit être lisible par quelqu'un qui ne fait pas de SEO.

## Prérequis

Ce skill exige le MCP SEO Cartograph. Si les outils (`get_analytics_history`,
`get_tracked_positions`…) ne sont pas disponibles, ne pas simuler : expliquer en trois
lignes que le bilan se construit sur les données réelles du compte (Search Console, GA4,
rank tracker) et qu'il faut connecter le MCP depuis app.tnedjar.com, puis s'arrêter là.

## Étape 1 — Collecter (dans cet ordre, tout en lecture)

1. `list_crawl_sites` si le domaine n'est pas précisé — et le confirmer à l'utilisateur.
2. `get_analytics_history` (domaine, daily_days 30) — l'ossature du bilan :
   hebdo GSC (clics/impressions), hebdo GA4 (sessions/conversions), mensuel pour le
   recul, répartition des positions (top 3/10/20, position moyenne), quotidien pour
   dater précisément un décrochage ou un bond.
3. `get_tracked_positions` (domaine) — les mots-clés surveillés : position actuelle,
   Δ 7 jours, meilleure position, cannibalisation éventuelle (l'URL qui ranke n'est pas
   la cible).
4. `get_serp_reports` (domaine) — si des rapports SERP archivés existent sur deux dates,
   comparer : qui est entré/sorti du top 10 sur les clusters stratégiques.
5. `get_crawl_overview` (dernier crawl) — la santé technique en une ligne : nombre de
   pages, erreurs majeures, tendance vs crawl précédent si disponible.

## Étape 2 — Diagnostiquer (les règles de lecture)

- **Clics vs impressions** : impressions ↑ + clics → = problème de title/meta ou de
  position moyenne — pas un problème de contenu. Clics ↓ + impressions ↓ = perte de
  positions ou saisonnalité (vérifier le mensuel de l'an passé si disponible).
- **Répartition des positions** : le passage top 20 → top 10 est le signal d'effort qui
  paie ; le tassement du top 3 est l'alerte prioritaire (défendre avant de conquérir).
- **Conversions GA4 avant les sessions** : 1 000 sessions qui ne convertissent pas valent
  moins que 200 qui convertissent. Si conversions ↓ à sessions stables → problème de
  page ou d'offre, pas de SEO.
- **Cannibalisation** signalée par le tracker → action immédiate (c'est gratuit et rapide).
- Toujours dater les mouvements (le quotidien le permet) et chercher la cause dans ce qui
  a été fait ce mois-là — le bilan relie les actions aux effets, sinon il ne sert à rien.

## Étape 3 — Le rapport

Structure fixe, une page à l'écran, pas de jargon non expliqué :

```
# Bilan SEO — [domaine] — [mois année]

## L'essentiel (3 phrases max)
[Le mouvement dominant du mois, son ampleur chiffrée, et la priorité qui en découle.]

## Les chiffres
| Indicateur | Ce mois | Mois -1 | Tendance |
(clics GSC, impressions, sessions GA4, conversions, mots-clés top 3 / top 10 / top 20,
position moyenne)

## Ce qui a bougé
- 📈 [gains : mots-clés/pages, avec les chiffres]
- 📉 [pertes : idem — ne jamais les cacher, un rapport qui ne montre que le vert
  perd toute crédibilité]

## Pourquoi
[2-4 puces de diagnostic reliées aux actions du mois écoulé.]

## Les 3 actions du mois prochain
1. [Action précise + effet attendu + effort estimé]
2. …
3. …
```

En français par défaut, en anglais si l'utilisateur ou son client travaille en anglais.
Adapter le niveau : rapport pour client final = zéro acronyme sans explication ; rapport
pour un consultant = plus dense, mêmes sections.

## Étape 4 — Boucler

Si des mots-clés stratégiques découverts pendant l'analyse ne sont pas suivis, proposer
de les ajouter au tracker (`track_keywords`) pour que le bilan du mois prochain soit plus
riche. Si un cluster stratégique n'a pas de rapport SERP archivé, proposer d'en lancer un
(`analyze_cluster_serp`, ~12 crédits) pour créer le point de comparaison.
