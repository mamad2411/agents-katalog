Afficher le dashboard de qualité du projet.

## Usage
`/truth:dashboard`

## Instructions

1. Collecter les métriques du projet :
   - Score TypeScript (erreurs tsc)
   - Score ESLint (warnings/errors)
   - Couverture tests (Vitest)
   - Score Lighthouse (si disponible)
   - Bundle size (Vite build output)

2. Calculer les tendances :
   - ↗️ Amélioration
   - → Stable
   - ↘️ Déclin

3. Afficher le dashboard :
```
📊 Quality Dashboard — Aurion Studio

| Métrique | Score | Trend | Cible |
|----------|-------|-------|-------|
| TypeScript | X errors | ↗️/→/↘️ | 0 |
| ESLint | X warnings | ↗️/→/↘️ | 0 |
| Tests | X% coverage | ↗️/→/↘️ | 80% |
| Bundle | X MB | ↗️/→/↘️ | < 2MB |
| Security | X issues | ↗️/→/↘️ | 0 |

Score global: X/10
```
