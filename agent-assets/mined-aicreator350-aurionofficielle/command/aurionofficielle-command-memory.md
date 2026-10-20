Gérer la mémoire collective de la hive.

## Usage
`/hive:memory [action]`

## Actions
- `show` — Afficher les entrées récentes
- `search [query]` — Chercher dans la mémoire
- `prune` — Nettoyer les entrées obsolètes
- `export` — Exporter en JSON
- `stats` — Statistiques d'utilisation

## Instructions

1. Exécuter l'action demandée sur la mémoire collective
2. Types de mémoire gérés :
   - **knowledge** — Faits appris pendant la session
   - **context** — Contexte de travail actuel
   - **task** — État des tâches assignées
   - **result** — Résultats des agents
   - **consensus** — Décisions votées
3. Afficher les résultats de manière structurée
4. Pour le pruning, garder seulement les entrées avec score > 0.5
