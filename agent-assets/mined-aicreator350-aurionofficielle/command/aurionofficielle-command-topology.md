Changer la topologie du swarm actif.

## Usage
`/swarm:topology [mesh|hierarchical|adaptive]`

## Instructions

1. Évaluer la topologie actuelle et ses performances
2. Appliquer la nouvelle topologie demandée :
   - **mesh** — Communication directe entre tous les agents, idéal pour tâches indépendantes
   - **hierarchical** — Un orchestrateur coordonne les workers, idéal pour tâches séquentielles
   - **adaptive** — Bascule dynamiquement selon la charge, idéal pour tâches complexes
3. Réassigner les rôles si nécessaire
4. Vérifier que la transition n'interrompt pas les tâches en cours
5. Confirmer la nouvelle topologie avec statut de chaque agent
