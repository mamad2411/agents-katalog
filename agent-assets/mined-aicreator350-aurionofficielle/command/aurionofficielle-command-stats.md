Afficher les statistiques de la mémoire des agents.

## Usage
`/memory:stats`

## Instructions

1. Compter les entrées par namespace et type
2. Calculer l'utilisation mémoire totale
3. Identifier les entrées les plus consultées
4. Identifier les entrées obsolètes (> 30 jours, jamais consultées)
5. Afficher les métriques de cache (hit rate, miss rate)

## Format de sortie
```
📊 Memory Stats

| Namespace | Entrées | Taille | Dernière MAJ |
|-----------|---------|--------|--------------|
| knowledge | N       | Xkb    | date         |
| patterns  | N       | Xkb    | date         |
| ...       | ...     | ...    | ...          |

Total: [N] entrées — [X]kb
Cache hit rate: [X]%
Entrées obsolètes: [N] (recommandé: /memory:cleanup)
```
