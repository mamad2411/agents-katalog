# Test Coverage

Analyse et améliore la couverture de tests.

## Instructions

1. **Mesure actuelle**
   - Lance `npx vitest run --coverage` pour le landing/dashboard
   - Pour les outils : `cd tools-deploy/[outil] && npx vitest run --coverage`
   - Note les fichiers avec <80% de couverture

2. **Identification des gaps**
   - Fichiers critiques sans tests :
     - api/_lib/middleware.ts (auth, CSRF, rate-limit)
     - api/_lib/credits.ts (deduct, reconcile)
     - src/lib/security/*.ts (sanitize, encrypt, csrf)
   - Composants UI sans tests visuels
   - Hooks custom sans tests

3. **Priorisation**
   - P0 : Sécurité (auth, CSRF, sanitization)
   - P1 : Business logic (crédits, paiements)
   - P2 : API handlers
   - P3 : Composants UI

4. **Génération ciblée**
   - Crée les tests manquants par priorité
   - Chaque test valide le comportement + les erreurs
   - Mock les dépendances externes

5. **Rapport**
   - Couverture avant/après par catégorie
   - Fichiers toujours non couverts (avec justification)
