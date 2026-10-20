Afficher les patterns découverts par le système d'apprentissage.

## Usage
`/training:patterns`

## Instructions

1. Analyser les trajectoires enregistrées
2. Identifier les séquences d'opérations récurrentes
3. Calculer le taux de succès de chaque pattern
4. Afficher les patterns triés par confiance

## Format
```
🧠 Patterns Découverts — [N] patterns, [M] trajectoires

| Pattern | Fréquence | Succès | Confiance |
|---------|-----------|--------|-----------|
| Feature dev: read→design→code→test | 12x | 83% | 0.85 |
| Bug fix: reproduce→trace→fix→verify | 8x | 91% | 0.90 |
| ...     | ...       | ...    | ...       |

Meilleur pattern pour votre type de tâche: [suggestion]
```
