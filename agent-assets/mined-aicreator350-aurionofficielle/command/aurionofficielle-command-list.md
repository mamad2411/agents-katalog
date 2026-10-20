Lister tous les agents actifs.

## Usage
`/agents:list`

## Instructions

1. Scanner les agents actifs dans la session
2. Afficher pour chaque agent :
   - ID et type
   - Tâche assignée
   - Statut (idle, working, done, failed)
   - Truth-score courant
   - Temps d'exécution

## Format
```
🤖 Agents Actifs — [N] agents

| ID | Type | Tâche | Statut | Score | Temps |
|----|------|-------|--------|-------|-------|
| 1  | coder | ... | 🔄 | 0.92 | 2m |
| 2  | tester | ... | ✅ | 0.95 | 1m |
| ...| ... | ... | ... | ... | ... |
```
