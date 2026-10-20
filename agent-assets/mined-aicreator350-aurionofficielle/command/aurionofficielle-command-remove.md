Retirer un agent de la session active.

## Usage
`/agents:remove [agent-id]`

## Instructions

1. Vérifier que l'agent existe
2. Si l'agent a une tâche en cours :
   - Sauvegarder l'état de progression
   - Proposer de réassigner la tâche
3. Retirer l'agent du pool actif
4. Libérer les ressources associées
5. Confirmer la suppression
