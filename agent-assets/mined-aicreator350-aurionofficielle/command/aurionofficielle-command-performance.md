Afficher les métriques de performance des agents.

## Usage
`/agents:performance`

## Instructions

1. Collecter les métriques de tous les agents (actifs + terminés)
2. Calculer par agent :
   - Taux de succès des tâches
   - Truth-score moyen
   - Temps moyen d'exécution
   - Nombre de rollbacks
3. Calculer les métriques globales :
   - Score moyen du pool d'agents
   - Agent le plus performant
   - Types de tâches les plus réussis

## Format
```
📈 Agent Performance

| Agent | Type | Tâches | Succès | Score Moy | Temps Moy |
|-------|------|--------|--------|-----------|-----------|
| ...   | ...  | ...    | ...    | ...       | ...       |

Meilleur agent: [type] — Score: [X]
Meilleur domaine: [type de tâche] — Succès: [X]%
```
