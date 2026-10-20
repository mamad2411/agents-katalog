Calculer le truth-score d'un morceau de code ou d'un changement.

## Usage
`/truth:score [fichier ou code]`

## Instructions

1. Analyser le code selon 5 dimensions :
   - **Correctness** (0.0-1.0) — Logique, types, gestion d'erreurs
   - **Security** (0.0-1.0) — OWASP, CSRF, injection, secrets
   - **Performance** (0.0-1.0) — Complexité, mémoire, renders
   - **Best Practices** (0.0-1.0) — SOLID, DRY, patterns Aurion
   - **Documentation** (0.0-1.0) — Types clairs, API docs, comments si nécessaire

2. Calculer le score pondéré :
   - Security × 0.30
   - Correctness × 0.25
   - Performance × 0.20
   - Best Practices × 0.15
   - Documentation × 0.10

3. Afficher le résultat :
   - ⭐ ≥ 0.95 — Excellent, production-ready
   - ✅ 0.85-0.94 — Bon, acceptable
   - ⚠️ 0.75-0.84 — Attention requise
   - ❌ < 0.75 — Critique, rework nécessaire

## Scoring honnête — pas de scores gonflés.
