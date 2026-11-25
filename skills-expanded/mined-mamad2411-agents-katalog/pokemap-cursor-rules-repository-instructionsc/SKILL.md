---
description: Sources obligatoires racine — AGENTS.md et codex_rule.md
alwaysApply: true
---

# Instructions dépôt (racine)

## Fichiers canoniques à respecter

Deux documents à la **racine du dépôt** priment sur les mémoires `.cursor/*.md` lorsqu’ils entrent en conflit (sauf instruction utilisateur plus spécifique) :

1. **`AGENTS.md`** — Périmètre monorepo Dart/Flutter, frontières de packages, Surface Engine, matrice de validation (`dart test` / `flutter test` / analyse), génération de code, hygiène de fichiers, compétences agents (superpowers, karpathy-guidelines) et rituels de review.

2. **`codex_rule.md`** — Règles Codex pour les lots : droit de remise en cause du prompt, audit obligatoire, sub-agents / passes nommées, commentaires utiles, rapport final détaillé, tests obligatoires, build ou alternative, critique finale, honnêteté sur les résultats.

## Comment les utiliser dans Cursor

- Avant un changement **non trivial** : relire les sections pertinentes d’`AGENTS.md` (boundaries, lot Surface si applicable, validation).
- Pour un **lot** ou un livrable type rapport + tests : appliquer **`codex_rule.md`** en plus du rituel **`.cursor/rules/codex-lot-workflow.mdc`** (les deux se renforcent ; le détail contractuel des lots est dans `codex_rule.md`).

## Priorité (rappel)

1. Requêtes explicites de l’utilisateur  
2. **`AGENTS.md`** et **`codex_rule.md`**  
3. Règles `.cursor/rules/*.mdc` et mémoires `.cursor/*.md`  
4. Comportement par défaut de l’agent

Ne pas supposer le contenu de ces fichiers : en cas de doute, **ouvrir et citer** les chemins exacts plutôt que d’inventer des conventions.
