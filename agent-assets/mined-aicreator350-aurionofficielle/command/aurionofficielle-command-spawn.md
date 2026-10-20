Spawner un agent spécialisé pour une tâche.

## Usage
`/agents:spawn [type] [tâche]`

## Types d'agents
- `researcher` — Explore le code, lit la doc, collecte le contexte
- `coder` — Implémente en TypeScript strict
- `tester` — Écrit et exécute les tests Vitest/Playwright
- `reviewer` — Review sécurité + qualité
- `optimizer` — Analyse et optimise les performances
- `architect` — Design patterns et architecture
- `documenter` — Documentation API et guides
- `security` — Audit sécurité OWASP

## Instructions

1. Créer l'agent du type demandé
2. Charger le contexte approprié (CLAUDE.md, fichiers pertinents)
3. Assigner la tâche décrite
4. Lancer l'exécution avec truth-score enabled
5. Retourner les résultats avec métriques
