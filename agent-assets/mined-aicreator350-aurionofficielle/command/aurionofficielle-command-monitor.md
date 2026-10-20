Surveiller un swarm en temps réel et intervenir si nécessaire.

## Usage
`/swarm:monitor`

## Instructions

1. Vérifier la santé de chaque agent :
   - Temps d'exécution vs estimation
   - Taux d'erreurs
   - Utilisation mémoire
2. Détecter les agents bloqués (> 2x temps estimé)
3. Vérifier la coordination inter-agents (pas de conflits)
4. Proposer des interventions si problèmes détectés :
   - Relancer un agent en échec
   - Redistribuer une tâche à un autre agent
   - Ajuster la topologie si nécessaire
5. Afficher les métriques de performance du swarm

## Alertes
- ⚠️ Agent en retard (> 1.5x temps estimé)
- 🔴 Agent en échec (erreur fatale)
- 🟡 Conflit détecté (même fichier modifié par 2 agents)
- ✅ Swarm sain (tous les agents progressent normalement)
