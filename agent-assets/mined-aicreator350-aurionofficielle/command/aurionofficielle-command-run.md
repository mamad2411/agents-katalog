Exécuter un workflow SPARC complet : Specification → Pseudocode → Architecture → Refinement → Completion.

## Usage
`/sparc:run [description de la tâche]`

## Instructions

1. **SPECIFICATION** — Analyser et documenter les exigences
   - Lire le contexte (CLAUDE.md, PROGRESS.md, gaps.md)
   - Identifier les contraintes techniques Aurion
   - Définir les critères d'acceptation
   - Estimer la complexité

2. **PSEUDOCODE** — Concevoir la solution en pseudo-code
   - Écrire l'algorithme en langage naturel
   - Identifier les types TypeScript nécessaires
   - Planifier les appels API et queries Supabase
   - Définir les composants React nécessaires

3. **ARCHITECTURE** — Structurer l'implémentation
   - Choisir les patterns (hooks, services, composants)
   - Planifier la structure des fichiers
   - Identifier les dépendances entre modules
   - Vérifier la conformité avec l'architecture Aurion

4. **REFINEMENT** — Implémenter et itérer
   - Coder en TypeScript strict (zero `any`)
   - Implémenter les tests (Vitest + Playwright)
   - Vérifier sécurité (CSRF, XSS, RLS)
   - Optimiser performance

5. **COMPLETION** — Finaliser et livrer
   - Run typecheck + lint + tests
   - Vérifier zéro erreur console
   - Mettre à jour PROGRESS.md
   - Déployer si tout est vert
