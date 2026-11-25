---
name: tuck-bit-fr
description: "TuckBit est une compétence portable pour les agents de programmation. Elle aide à sélectionner le bon contexte, les bons outils et les vérifications nécessaires sans compromettre la justesse."
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: fr
---

# TuckBit — Français

> Le cœur de la compétence est traduit; les références techniques restent provisoirement en anglais et nécessitent une révision communautaire.

Optimisez les résultats corrects et vérifiés par ressource consommée, plutôt que le seul nombre de jetons.

Quatre fonctions par défaut : registre, contexte, vérification et budget. Orchestration et métriques sont facultatives.

## Méthode de travail

Partez de la demande exacte, des instructions réellement disponibles et des outils autorisés. Préservez toutes les contraintes, validations et vérifications exigées.

1. Définissez le résultat attendu, les contraintes, les risques et une condition d'arrêt; évitez la planification excessive pour les tâches simples.
2. Repérez le code, la documentation et les outils pertinents les plus ciblés; élargissez seulement si nécessaire.
3. Préférez la découverte native des outils; les métadonnées ne constituent jamais une autorisation d'exécution.
4. Utilisez un seul agent pour les petites tâches; répartissez les travaux indépendants avec des responsabilités et critères explicites.
5. Lancez les tests ciblés, puis les contrôles d'intégration et de sécurité requis sur la révision finale.
6. Produisez un compte rendu vérifiable des modifications, tests, risques et blocages. Enregistrez des jalons et évitez les consultations répétitives.

## Chargez uniquement la référence utile

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## Limites impératives

Ne sautez pas les contrôles de sécurité, ne dégradez pas la qualité, n'inventez pas de résultats, ne lisez pas de secrets et ne contournez pas les autorisations. L'hôte conserve le contrôle des permissions.

**Aperçu développeur. L'installation ne prouve ni l'activation réelle ni une économie de jetons.**
