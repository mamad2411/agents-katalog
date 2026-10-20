Stocker une information dans la mémoire persistante des agents.

## Usage
`/memory:store [clé] [valeur]`

## Instructions

1. Déterminer le type de mémoire approprié :
   - **knowledge** — Faits techniques, conventions de code
   - **context** — Contexte de travail en cours
   - **pattern** — Patterns réutilisables découverts
   - **decision** — Décisions architecturales prises
2. Stocker avec la clé fournie dans le namespace approprié
3. Ajouter métadonnées : timestamp, confidence score, source
4. Confirmer le stockage avec résumé

## Namespaces Aurion
- `memory/auth/` — Patterns d'authentification Clerk
- `memory/credits/` — Logique crédits et billing
- `memory/tools/` — Configuration par outil
- `memory/patterns/` — Patterns réutilisables
- `memory/decisions/` — Architecture Decision Records
