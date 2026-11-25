---
name: unit-test-task-generator
description: Generate backend unit and integration test task markdown after implementation tasks exist. Use during SDD planning for PHPUnit/Laravel or equivalent backend test coverage per feature — not for E2E (use e2e-test-generator). Requires requirements and related backend task. Documents cross-tenant and auth P0 scenarios when applicable.
---

# Unit Test Task Generator

Create `task-NNN-*.md` for backend unit and HTTP integration tests covering a Feature.

## Boundary

- **Planning:** this skill (task markdown)
- **Execution:** implement tests per task — use `coder` or implementation workflow

## Harness discovery

Load `{harness}/rules/backend-tests-rules.mdc` and `backend-rules.mdc` when present.

## Inputs

- Feature to cover
- List of backend implementation tasks already generated
- `requirements.md` data model

## Test pyramid (backend)

```
        [ E2E ]  ← e2e-test-generator
     [ Integration ]  ← Controller/HTTP tests
    [ Unit tests ]  ← Service, FormRequest, Model, Rules
```

## What to test

| Component | Type | Focus |
|-----------|------|-------|
| FormRequest | Unit | Valid/invalid fields, tenant FK rules |
| Service | Unit | Business logic, mocks |
| Model | Unit | Scopes, casts, relations |
| Controller | Integration | Status, response shape, auth, 401/403 |
| Tenant scope | Integration | Cross-tenant P0 — never 200 for other company |

## Output structure

See factory pattern in skill body — include:

- Summary and detailed test plan (not duplicate)
- Files under `tests/Unit/` and `tests/Feature/`
- Scenario checklists per component
- Mandatory patterns: RefreshDatabase, factories, response shape, cross-tenant cases

## Dependencies

Task must reference `task-NNN.md` of the backend implementation it covers.

## Rules

- Happy-path-only tasks for tenant-scoped CRUD are **incomplete** without cross-tenant P0
- Do not point tests at production database
- Match project's test runner commands (e.g. `php artisan test`)

## Related skills

- `task-generator` — implementation tasks first
- `e2e-test-generator` — UI coverage
