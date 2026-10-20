Analyser un fichier ou module avec le pipeline d'analyse.

## Usage
`/stream:analysis [cible]`

## Instructions

1. **Scan structurel** — Mapper les exports, imports, dépendances
2. **Détection d'issues** — TypeScript errors, patterns anti, complexité
3. **Évaluation sécurité** — Inputs non sanitizés, secrets exposés
4. **Évaluation performance** — Renders inutiles, queries lourdes
5. **Recommandations** — Actions priorisées avec estimations d'effort

## Format
```
📊 Analyse: [cible]

Structure: [X] exports, [Y] imports, complexité [Z]
Issues: [N] critiques, [N] warnings
Sécurité: [score]/10
Performance: [score]/10

Top 5 recommandations:
1. [action] — Impact: [high/medium/low]
2. ...
```
