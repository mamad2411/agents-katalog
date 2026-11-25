---
name: pm-e2e-test-generator
description: (NS) Generate E2E test task markdown for Cypress/TypeScript during SDD planning after frontend tasks exist. Use when planning Cypress coverage per feature — not for writing specs (use code-e2e-tests). Requires data-testid contract from frontend task. Device-aware desktop/tablet/mobile structure.
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
---

# E2E Test Task Generator

Planning-phase skill: produce E2E task markdown. Execution-phase: `code-e2e-tests`.

## Boundary

| Phase                         | Skill                |
| ----------------------------- | -------------------- |
| Planning (task file)          | `pm-e2e-test-generator` |
| Implementation (Cypress code) | `code-e2e-tests`   |

## Harness discovery

Load `{harness}/rules/e2e-tests-rules.mdc` and `frontend-rules.mdc` when present.

## Inputs

- Feature to cover
- Frontend implementation task(s) with **data-testid contract**
- If contract missing → stop and request frontend task update

## E2E project location

Default (greenfield): **`{product_root}/tests-e2e/`** — independent Node package; paths below are relative to that root.

Brownfield: use detected Cypress root (`tests-e2e/`, legacy `testes-cypress/`, or `frontend/`). Do not plan new specs under `frontend/cypress/` when no E2E exists yet.

## Output highlights

Task file must include:

- Summary and detailed coverage strategy
- **E2E root** — `tests-e2e/` (or detected brownfield path)
- **data-testid contract table** (copied from frontend task — do not invent)
- Spec paths under `tests-e2e/cypress/e2e/device/{desktop|tablet|mobile}/[feature]/` (adjust prefix if brownfield)
- Command files under `tests-e2e/cypress/support/commands/` — `shared/`, `pages/`, `device/`
- Bootstrap note when project has no E2E yet: executor must run `code-e2e-tests` Phase 0 before specs
- Success, error, and **RBAC by URL** scenarios
- Device coverage matrix
- Validation criteria: no fixed `cy.wait(N)`, commands not DOM in specs, `@smoke`/`@regression` tags

## Dependencies

Depends on frontend implementation task for the same feature.

## Docker note

When E2E runs in container: API URL via host gateway, not `localhost` inside container — per infra rules when present.

## Related skills

- `code-e2e-tests` — write/refactor Cypress code
- `pm-task-generator` — frontend tasks with testid contract
