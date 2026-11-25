---
name: rapport-client
description: >
  Assemble le grand rapport SEO client (livrable complet, marque blanche possible) à partir
  de toutes les données RÉELLES du compte SEO Cartograph (MCP requis) : performance Search
  Console et GA4, évolution des positions, santé technique du crawl, opportunités priorisées,
  face-à-face concurrents. Un document structuré, lisible par un décideur, avec synthèse
  exécutive et feuille de route. Utiliser ce skill dès que l'utilisateur demande « le rapport
  client », « le reporting complet », « prépare le livrable pour mon client », « rapport SEO
  trimestriel », « bilan complet », ou veut un document de synthèse à présenter — même sans
  le mot « rapport ». Nécessite le MCP SEO Cartograph connecté. Pour un point mensuel court,
  préférer le skill bilan-seo-mensuel.
---

# Rapport client — le livrable qui se présente

C'est le document qu'un consultant pose devant son client, ou qu'un responsable montre à sa
direction. Il ne liste pas des métriques : il raconte une histoire — où on en est, ce qui a
bougé et pourquoi, ce qu'on va faire. La synthèse exécutive se lit en 30 secondes et se
suffit à elle-même ; le détail est là pour ceux qui creusent. Zéro jargon non expliqué.

## Prérequis

MCP SEO Cartograph connecté. Sans les outils, ne pas fabriquer un rapport sur des données
inventées : expliquer qu'il s'assemble sur les données réelles du compte et inviter à
connecter le MCP. Puis s'arrêter. (Ce skill demande beaucoup d'outils — vérifier
`get_serp_credits` si un face-à-face concurrents ou des analyses SERP sont prévus.)

## Étape 1 — Cadrer le rapport

Verrouiller : la **période** (mois, trimestre), le **destinataire** (client final PME =
zéro acronyme, langage résultats ; direction = ROI et priorités ; équipe SEO = dense), la
**langue**, et la **marque blanche** (si l'utilisateur est une agence, demander logo/nom à
faire figurer — sinon en-tête neutre). Confirmer le domaine.

## Étape 2 — Rassembler (l'ordre du récit)

1. `get_analytics_history` (domaine, daily_days selon période) — la performance : trafic
   GSC (clics/impressions), GA4 (sessions/conversions), mensuel pour le recul, répartition
   des positions. C'est l'ossature « où on en est ».
2. `get_tracked_positions` — les mots-clés stratégiques : gains et pertes, Δ, meilleures
   positions.
3. `get_crawl_overview` (dernier crawl) — la santé technique : une section courte, tendance
   vs crawl précédent si dispo.
4. `get_search_queries` — la matière pour la section opportunités (positions 4-20).
5. `get_serp_reports` — s'ils existent, l'évolution de la SERP sur les clusters clés
   (face-à-face concurrents). Ne pas lancer d'analyses coûteuses sans le dire (crédits).
6. `get_clusters_data` — pour situer les recommandations dans les cocons.

Ne pas tout mettre : sélectionner ce qui sert le récit. Un rapport de 40 tableaux ne se lit
pas ; un rapport de 5 sections nettes se présente.

## Étape 3 — Le document

```
# Rapport SEO — [client / domaine] — [période]
[En-tête marque blanche si agence]

## Synthèse exécutive
[4-6 phrases qui se suffisent : la tendance dominante chiffrée, la victoire du trimestre,
le point de vigilance, et la priorité n°1. Un décideur qui ne lit QUE ça doit repartir avec
le bon message.]

## 1. Performance
| Indicateur | Période | Période précédente | Évolution |
(clics, impressions, sessions, conversions, top 3 / top 10 / top 20, position moyenne)
[+ lecture : ce que ces chiffres racontent, en clair — pas juste le tableau.]

## 2. Positions
- 📈 Gains marquants [mots-clés/pages, avec les chiffres]
- 📉 Pertes [assumées, jamais cachées — la crédibilité en dépend]
[+ le diagnostic : pourquoi ces mouvements, reliés aux actions de la période.]

## 3. Santé technique
[État en quelques lignes : ce qui est sain, le poste d'erreur dominant s'il y en a un,
la tendance. Le détail complet relève du skill audit-technique — ici on synthétise.]

## 4. Concurrence (si données SERP)
[Part de voix sur les clusters clés, mouvements des concurrents suivis. Sinon, sauter la
section proprement plutôt que la remplir de vide.]

## 5. Opportunités & feuille de route
[Les 3 à 5 chantiers prioritaires du trimestre suivant, chacun avec : l'objectif, l'effort,
le gain attendu. C'est la section qui justifie la prestation — la plus soignée.]

## Annexe (optionnelle)
[Tableaux détaillés pour qui veut vérifier — hors du corps du rapport.]
```

## Étape 4 — Soigner la présentation

- **Le rendu** : proposer à l'utilisateur le format qui l'arrange. Markdown pour coller/
  éditer, ou HTML autonome propre s'il veut l'imprimer en PDF (via l'impression du
  navigateur) ou l'envoyer tel quel. En HTML, soigner l'en-tête (marque blanche), la
  lisibilité des tableaux, et un style sobre imprimable.
- **Les chiffres parlent en tendance** : toujours un comparatif (vs période précédente),
  toujours une flèche, jamais un nombre nu.
- **Honnêteté** : montrer les pertes. Un rapport tout-vert perd la confiance du client dès
  qu'il croise sa propre Search Console.

## Étape 5 — Enchaîner

Ce rapport est une synthèse ; chaque section a son skill d'approfondissement si le client
veut creuser : audit-technique (section 3), opportunites-seo (section 5), face-à-face
détaillé via analyze_cluster_serp (section 4). Le proposer en conclusion, pas l'imposer.
