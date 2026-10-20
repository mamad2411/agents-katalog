Analyser et reviewer une Pull Request GitHub.

## Usage
`/github:pr-review [PR number ou URL]`

## Instructions

1. Récupérer les détails de la PR (fichiers changés, diff, description)
2. Évaluer la PR selon :
   - Qualité du code (TypeScript strict, patterns Aurion)
   - Impact sécurité (CSRF, RLS, sanitization)
   - Impact performance (bundle size, render cycles)
   - Couverture tests (nouveaux tests pour nouveau code)
   - Documentation (changelog, API docs si pertinent)
3. Classifier les issues par sévérité
4. Générer un commentaire de review structuré
5. Recommander : Approve / Request Changes / Comment
