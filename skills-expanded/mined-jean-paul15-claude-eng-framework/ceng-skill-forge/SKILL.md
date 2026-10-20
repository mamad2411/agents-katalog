---
name: ceng-skill-forge
description: Création et amélioration contrôlée des skills du projet à partir de l'expérience (rétrospective après une tâche importante, leçons répétées, brouillons de skills générés par ceng init à compléter par recherche). Empêche qu'une expérience isolée devienne une règle globale.
---

# Skill forge — auto-amélioration contrôlée

## Après une tâche importante (rétrospective, 5 minutes max)
Réponds brièvement : qu'est-ce qui a fonctionné ? échoué ? quelle erreur se répète ? quelle décision a été
efficace ? quelle procédure est réutilisable ? Consigne chaque élément utile :
`node .ceng/runtime/cli.js learn add --kind worked|failed|recurring-error|effective-decision|procedure --topic "<clé stable>" --lesson "…" --task T-xxxx [--source <URL officielle>] [--skill <skill visée>]`
Utilise une **clé de sujet stable** (ex. `prisma-migration-shadow-db`) pour que les répétitions se regroupent.

## Promotion d'une leçon en règle
`node .ceng/runtime/cli.js learn promote` liste seulement les leçons :
- observées sur **≥ 3 tâches distinctes**, ou
- adossées à une **source primaire** (documentation officielle, RFC, avis de sécurité).
Une leçon isolée n'est jamais promue. Pour chaque candidate :
1. Choisis la cible : skill existante la plus proche (préférée) ou nouvelle skill si le domaine est distinct.
2. Écris la règle avec son **domaine de validité** et sa **contre-indication** (« quand ne pas l'appliquer »).
3. Garde la skill courte : une procédure, des heuristiques, des pièges. Détails → fichier annexe.
4. Autonomie ≠ `high` : présente le changement à l'humain avant de l'écrire. Toujours : `decision add` si la
   règle change une pratique d'équipe.

## Compléter un brouillon de skill projet (`metadata.ceng-status: draft`)
1. Délègue à `ceng-researcher` la section « Recherche à compléter » (sources officielles, versions du projet).
2. Remplace les affirmations non vérifiées ; ajoute les liens consultés avec la date.
3. Passe `ceng-status: verified`. Ne garde que ce qui sert aux tâches du projet.

## Créer une nouvelle skill
`node .ceng/runtime/cli.js skill new <nom> --description "…"` puis remplis. Règles d'écriture :
- description = quand l'utiliser, avec les mots que l'on emploie réellement (c'est elle qui déclenche le chargement) ;
- SKILL.md < 200 lignes ; instructions critiques en tête ; pas de duplication avec une autre skill ;
- ne jamais nommer une skill comme une commande intégrée (`code-review`, `security-review`, `init`, `simplify`…).

## Hygiène
`node .ceng/runtime/cli.js adapt` signale les skills jamais utilisées : propose à l'humain de passer leur
visibilité en `name-only` (`skillOverrides` dans .claude/settings.local.json) pour alléger le contexte.
