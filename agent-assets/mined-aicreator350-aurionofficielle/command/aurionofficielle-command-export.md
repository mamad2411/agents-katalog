Exporter les données d'apprentissage.

## Usage
`/training:export [format]`

## Formats
- `json` — Export JSON complet
- `markdown` — Rapport lisible
- `csv` — Données tabulaires

## Instructions

1. Collecter toutes les trajectoires et patterns
2. Formater selon le format demandé
3. Inclure :
   - Trajectoires avec scores
   - Patterns avec confiance
   - Statistiques agrégées
   - Recommandations
4. Sauvegarder dans `.research/training-export.[ext]`
