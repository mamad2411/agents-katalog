---
name: playwright-e2e
description: >-
  Optional stack skill: Playwright end-to-end tests. Use when writing,
  debugging, or verifying E2E coverage for QA handoff verification.
---

# Playwright E2E (optional)

Enable this skill when the project uses Playwright. Paths and package filters come from `.agents/skills/project-context/SKILL.md`.

## Workspace (typical)

| Item            | Location                   |
| --------------- | -------------------------- |
| Package         | `@your-scope/e2e` → `e2e/` |
| Specs & helpers | `e2e/src/`                 |
| Config          | `e2e/playwright.config.ts` |

Prefer keeping Playwright dependencies in the e2e package, not the monorepo root. Root may proxy scripts (`pnpm test:e2e`).

## Layout

```text
e2e/
  playwright.config.ts
  package.json
  src/
    pages/           # Page Object Model classes
    helpers/         # Cross-page utilities
    *.spec.ts
```

## Page Object Model (POM)

Follow [Playwright page object models](https://playwright.dev/docs/pom).

1. One class per page or wizard step group.
2. Constructor takes `Page`; store locators as `readonly`.
3. Prefer `getByTestId` when the app exposes `data-testid` (see optional `nextjs-frontend` skill).
4. Fallback: `getByRole` / visible copy for legacy screens.
5. Specs stay thin — orchestrate page objects and assert outcomes.

## Locator priority

1. `page.getByTestId('…')`
2. `getByRole` + name
3. Visible text (last resort — brittle when copy changes)

## Conventions for new tests

1. POM for new and extended flows.
2. Add matching `data-testid` in the UI in the same change.
3. Isolate session/storage in `beforeEach` when flows persist state.
4. Prefer serial workers unless storage/DB isolation is proven.
5. Assert URL + role/heading + at least one business signal.

## QA agent workflow

1. Map `03-acceptance-criteria.md` to existing specs; note gaps.
2. Ensure services/DB/browsers are ready; run the project’s e2e command.
3. Record command + pass/fail in `06-qa-report.md`.
4. On failure: capture failing spec, error snippet, and whether apps failed to start.

## Checklist

- [ ] Specs under e2e src; page objects for new flows
- [ ] Prefer `getByTestId` where available
- [ ] No Playwright dependency on monorepo root (unless project already does)
- [ ] E2E suite green locally
- [ ] New coverage noted in QA report and/or e2e README
