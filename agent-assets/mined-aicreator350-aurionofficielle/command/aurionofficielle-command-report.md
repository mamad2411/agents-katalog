Générer un rapport de qualité complet exportable.

## Usage
`/truth:report [format]`

## Formats
- `markdown` — Rapport Markdown (défaut)
- `json` — Export JSON pour CI/CD
- `html` — Rapport HTML avec graphiques

## Instructions

1. Exécuter toutes les vérifications :
   - TypeScript strict check
   - ESLint analysis
   - Test run + coverage
   - Security scan
   - Bundle analysis
   - Performance metrics

2. Agréger les résultats en rapport structuré
3. Inclure les recommandations prioritisées
4. Exporter dans le format demandé
5. Sauvegarder dans `docs/quality-report.[ext]`
