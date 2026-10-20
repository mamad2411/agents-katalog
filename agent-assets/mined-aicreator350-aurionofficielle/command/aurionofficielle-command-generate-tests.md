# Generate Test Cases

Génère des cas de test exhaustifs pour un module ou composant.

## Instructions

Paramètre : $ARGUMENTS (chemin du fichier ou module à tester)

1. **Analyse du code**
   - Lis le fichier source
   - Identifie les fonctions publiques, props, états
   - Identifie les edge cases et erreurs possibles

2. **Catégorisation des tests**
   - **Unit tests** : fonctions pures, utilitaires, hooks
   - **Integration tests** : composants avec state, API calls
   - **E2E tests** : workflows utilisateur

3. **Génération (Vitest pour Aurion)**
   - Import depuis `vitest` (describe, it, expect, vi)
   - Mock des services externes (Supabase, Clerk, Stripe)
   - Couverture des happy path ET error paths
   - Tests de types TypeScript implicites

4. **Patterns de test Aurion**
   - `vi.mock()` pour les modules
   - `renderHook()` pour les hooks custom
   - `render()` + `screen.getByRole()` pour les composants
   - `waitFor()` pour les opérations async

5. **Output**
   - Fichier `.test.ts` ou `.test.tsx` adjacent au source
   - Minimum 80% de couverture des branches
   - Tests indépendants (pas d'ordre requis)
