---
name: ns-code-e2e-tests
description: (NS) Create and maintain Cypress E2E tests in an independent tests-e2e/ Node package at product root (bootstrap when missing). DRY device-aware command architecture (shared/pages/device). Use when writing or refactoring Cypress specs, custom commands, scaffolding E2E on greenfield projects, or implementing E2E tasks — not when planning E2E task markdown (use ns-pm-e2e-test-task-generator). Read harness e2e rules when present. Mandatory discovery before writing specs.
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
---

# Create E2E Tests

Execution-phase Cypress implementation. Planning-phase: `ns-pm-e2e-test-task-generator`.

## Harness discovery

Load `{harness}/rules/e2e-tests-rules.mdc` when present. See `references/e2e-architecture.md` for layout and bootstrap summary.

## Phase 0 — Resolve or bootstrap Cypress root

**Before any spec or command code**, locate the Cypress project or create it.

### 0.1 — Detect existing E2E (brownfield)

Search `{product_root}` in this order:

1. `tests-e2e/cypress.config.ts`
2. `testes-cypress/cypress.config.ts` (legacy name)
3. `frontend/cypress.config.ts` (legacy co-located)

Record the directory that contains `cypress.config.ts` as **`{e2e_root}`**. All paths below are relative to `{e2e_root}` unless noted.

### 0.2 — Bootstrap when nothing exists (greenfield)

If no match in 0.1, create **`{product_root}/tests-e2e/`** as a **standalone Node project**:

| Rule | Detail |
| ---- | ------ |
| Location | `{product_root}/tests-e2e/` only |
| `package.json` | **Here** — never add Cypress to `frontend/package.json` |
| Tree | Per `references/e2e-architecture.md` (config + empty `device/` folders + support imports) |
| `cypress.config.ts` | `baseUrl` from `CYPRESS_BASE_URL`; `specPattern` `cypress/e2e/**/*.cy.ts` |
| Scripts | `cypress:open`, `cypress:run` in `tests-e2e/package.json` |

Then set `{e2e_root} = {product_root}/tests-e2e/`.

**Forbidden on greenfield:** scaffolding under `frontend/cypress/`, copying deps into the frontend lockfile, or assuming Cypress is already installed in the app package.

### 0.3 — Post-bootstrap documentation

When `{product_root}/docs/context/stack-confirmed.md` or `architecture-rules.md` exists, add or update the E2E row: location `tests-e2e/`, run command `cd tests-e2e && npm run cypress:run` (or project docker equivalent).

Do not proceed to Phase 1 until `{e2e_root}` is confirmed and `cypress.config.ts` is readable.

## Phase 1 — Discovery (before feature code)

1. **App under test** — routes, forms, API usage, existing `data-testid` (read `frontend/`, not write Cypress there)
2. **Existing commands** — read all `{e2e_root}/cypress/support/commands/`; never duplicate
3. **Config** — `{e2e_root}/cypress.config.ts` baseUrl, env vars (`CYPRESS_BASE_URL`, `CYPRESS_API_URL`)

## Phase 2 — Command architecture first

```
{e2e_root}/cypress/support/commands/
  shared/[feature].commands.ts   # business actions — all devices
  pages/[feature].commands.ts    # page structure
  device/mobile|tablet|desktop.commands.ts
```

| Behavior            | Location  |
| ------------------- | --------- |
| Same on all devices | `shared/` |
| Device-exclusive    | `device/` |
| Page DOM structure  | `pages/`  |

Register new command files in `{e2e_root}/cypress/support/e2e.ts`.

Specs: `describe`/`it`, `cy.visit()`, commands, assertions — **no DOM logic in specs**.

## Phase 3 — Spec layout

```
{e2e_root}/cypress/e2e/device/
  desktop/[feature]/[feature]-successful-flows.cy.ts
  tablet/...
  mobile/...
```

Viewports in `beforeEach`:

- Desktop: 1280×720
- Tablet: 768×1024
- Mobile: 375×812

Forbidden: specs directly under `cypress/e2e/` without `device/` prefix.

## Phase 4 — Implement

- Use `data-testid` from frontend task contract — do not invent
- No fixed `cy.wait(N)` — intercepts or assertion timeouts
- RBAC: menu hidden + direct URL denial
- Auth: login via UI or support session; tenant-aware fixtures

## Phase 5 — Run and report

From `{e2e_root}`: `npm run cypress:run` (or docker equivalent documented for the product). Report failures with `ns-code-investigator` if needed.

## References

| File                             | When                              |
| -------------------------------- | --------------------------------- |
| `references/e2e-architecture.md` | Root layout, bootstrap tree, rules |
| `ns-pm-e2e-test-task-generator`             | Task contract source              |

## Related skills

- `ns-pm-e2e-test-task-generator` — planning tasks with testid contract
- `ns-code-investigator` — failing E2E debugging
- `ns-gitlab-ci-generator` — CI `cd tests-e2e` and change paths
