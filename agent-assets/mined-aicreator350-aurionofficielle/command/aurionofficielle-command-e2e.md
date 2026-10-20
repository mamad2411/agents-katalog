# E2E Test Setup & Run

Setup et exécution des tests E2E Playwright.

## Instructions

1. **Vérification du setup**
   - Vérifie playwright.config.ts existe
   - Vérifie les browsers installés : `npx playwright install`
   - Vérifie le baseURL dans la config

2. **Tests existants (40+ specs)**
   - e2e/01-page-load.spec.ts → e2e/41-full-click-audit.spec.ts
   - Couvrent : navigation, hero, sections, FAQ, contact, pricing, auth, responsive, a11y, perf, SEO, security

3. **Exécution**
   - Run all : `npx playwright test`
   - Run specific : `npx playwright test e2e/01-page-load.spec.ts`
   - Run headed : `npx playwright test --headed`
   - Show report : `npx playwright show-report`

4. **Debug failed tests**
   - Trace viewer : `npx playwright test --trace on`
   - Screenshots auto dans test-results/
   - Debug mode : `npx playwright test --debug`

5. **Nouveaux tests**
   - Suivre le pattern existant (numérotation séquentielle)
   - Un spec par feature/workflow
   - Utiliser page.getByRole() en priorité
   - Assertions strictes (toBeVisible, toHaveText)
