Vérifier un changement de code contre les standards Aurion.

## Usage
`/truth:verify [fichier]`

## Instructions

1. Exécuter les vérifications automatiques :
   - `npx tsc --noEmit` — Zéro erreur TypeScript
   - `npx eslint --max-warnings 0` — Zéro warning ESLint
   - Tests unitaires pour les fichiers modifiés
   - Scan sécurité rapide

2. Vérifications manuelles :
   - Zero `any` dans le code TypeScript
   - CSRF token sur POST endpoints
   - Input sanitization via security utilities
   - Pas de secrets hardcodés
   - RLS policies si nouveau schema Supabase

3. Retourner PASS/FAIL avec détails :
   - ✅ PASS — Code vérifié et conforme
   - ❌ FAIL — Issues trouvées (listées avec fixes)
