Exécuter le pipeline de test automatique.

## Usage
`/stream:test [cible]`

## Instructions

1. **Couverture** — Analyser la couverture existante avec Vitest
2. **Gaps** — Identifier les fonctions/composants non testés
3. **Génération** — Créer les tests manquants (Vitest pour unit, Playwright pour E2E)
4. **Exécution** — Lancer la suite complète
5. **Rapport** — Afficher couverture avant/après

## Contraintes Aurion
- Tests unitaires : Vitest + React Testing Library
- Tests E2E : Playwright (42 specs dans `e2e/`)
- Mocks : MSW pour les appels API
- Coverage cible : > 80%
