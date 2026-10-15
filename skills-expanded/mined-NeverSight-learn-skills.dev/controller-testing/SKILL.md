---
name: controller-testing
description: "Writes Pest feature tests for Laravel HTTP controllers with repeatable patterns for web/session and API/JSON flows. Activates for controller-focused feature tests (especially under tests/Feature/Http/Controllers/**), CRUD action matrices, nested route binding checks, authorization outcomes (403 vs 404), validation datasets, and persistence assertions. Takes precedence over pest-testing for controller-focused feature tests."
license: MIT
metadata:
  author: Hosmel Quintana
---

# Controller Testing

## When to Apply

Activate this skill only when the task is about **Laravel controller feature tests** (action-level HTTP behavior for a controller) and includes signals like:

- The test file path is under `tests/Feature/Http/Controllers/**` (including `tests/Feature/Http/Controllers/Api/**`). This is the primary trigger.
- The task is explicitly about a controller action and uses action-level `describe('create' | 'destroy' | 'edit' | 'index' | 'show' | 'store' | 'update')`.
- Controller route assertions using `route(...)`, nested parameters, and route-model binding scope checks.
- Auth/authorization outcomes and controller transport assertions:
  - web/session (`get`, `post`, `patch`, `delete`, `assertInertia`, redirects), or
  - API/JSON (`getJson`, `postJson`, `patchJson`, `deleteJson`, JSON assertions).

Do not activate this skill based on `describe('store')` alone (many non-controller feature tests use the same verbs, for example Fortify/auth flows).

Do **not** use this skill for model/unit tests, service-layer tests, console commands, or non-HTTP behavior.

## Kill Switch / Precedence

For controller-focused feature tests, this skill takes precedence over `pest-testing`.
If `pest-testing` was selected for controller test work, stop and switch to `controller-testing` immediately.

## Quick Start

```bash
# Create file only when needed
php artisan make:test --pest Http/Controllers/<Name>ControllerTest --no-interaction

# Run only the affected file
php artisan test --compact tests/Feature/Http/Controllers/<Name>ControllerTest.php

# Optional focused rerun
php artisan test --compact --filter="<test name>"
```

## Decision Workflow

1. Inspect the controller action, form request, policy, resource, and route definition to derive the contract under test.
2. Choose transport mode: web/session or API/JSON.
3. Determine route shape (flat vs nested) and parameter keys.
4. For each action under test, apply this baseline in order (as applicable):
   - requires authentication
   - policy denial (`403`)
   - binding mismatch (`404`)
   - validation datasets (`store`/`update`)
   - success response + persistence assertions
5. Load only the reference files needed for the action/rule pattern.

## Output Guardrails (Keep Controller Tests Clean)

These guardrails exist to prevent noisy, inconsistent tests.

- Treat the controller contract as the source of truth. Templates are starting points only; adapt them to the actual request payload, response shape, redirects, resources, and policy flow implemented by the controller.
- Keep `403` tests minimal. For forbidden cases, you usually do not need to send a full payload (authorization should fail before validation).
- Validation datasets must be small and stable:
  - Each dataset `data` should only include the field(s) needed to trigger that rule. Do not repeat a full "valid payload" for every case.
  - Assert validation messages for every failing field. Do not use keys-only expectations in these datasets.
  - When multiple fields share a `sometimes|required`-style blank-value rule, prefer one dataset case that submits blank strings for all of those fields and asserts the required message for each of them. Do not reduce that pattern to a single representative field.
  - Prefer `post(...)`/`patch(...)` directly; avoid `from(...)` unless you cannot get a reliable redirect-back assertion otherwise.
- Prefer route-based redirects: use `assertRedirectToRoute(...)` when a named route exists; use `assertRedirect(...)` only when the destination is not a named route or is config-driven.

## Canonical `403` vs `404` Rule

Use this as the source of truth:

- If route bindings resolve correctly and authorization denies access, assert `assertForbidden()` (`403`).
- If route-model binding fails (wrong parent/child chain, scoped binding mismatch), assert `assertNotFound()` (`404`).

Actor context to keep outcomes deterministic:

- `403` tests: authenticate an **in-scope actor** that can resolve bindings but lacks permission.
- Validation and success-path tests: authenticate an **authorized in-scope actor**.
- `404` binding-mismatch tests: any authenticated actor is acceptable because binding fails first.

## Reference Map

Load only what you need:

- API/JSON adaptation guide and full examples:
  - `references/modes/api-json.md`
- Nested route naming and parameter composition:
  - `references/route-patterns.md`
- Per-action templates (web/session-first):
  - `references/actions/create.md`
  - `references/actions/destroy.md`
  - `references/actions/edit.md`
  - `references/actions/index.md`
  - `references/actions/show.md`
  - `references/actions/store.md`
  - `references/actions/update.md`
- Validation catalogs (merge only required rules):
  - `references/validation/store-validates-fields.md`
  - `references/validation/update-validates-fields.md`
- Focused validation patterns (prefer first when matching rules exist):
  - `references/validation/required-with-and-array.md`
  - `references/validation/scoped-exists-and-unique.md`
  - `references/validation/prepare-for-validation.md`
  - `references/validation/api-login-validation.md`

Action references are web/session-first templates. For API/JSON controllers, keep the same action structure and adapt assertions with `references/modes/api-json.md` based on the controller/resource contract under test.

## Baseline Assertions by Transport

Web/session mode:

- `requires authentication` -> redirect to login route.
- Validation failures -> `assertRedirectBackWithErrors(...)`.
- Page actions -> `assertOk()` + `assertInertia(...)`.
- Mutation actions -> redirect + persistence assertions.
- Toast/flash assertions are optional and app-specific.

API/JSON mode:

- Protected endpoints: `requires authentication` -> `assertUnauthorized()`.
- Public endpoints: skip auth-required test unless the endpoint is protected.
- Validation failures -> `assertUnprocessable()` + `assertJsonValidationErrors(...)`.
- Success actions -> `assertOk()` / `assertCreated()` / `assertNoContent()` + JSON + persistence assertions.
- Assert validation messages, not just keys, so the test verifies the exact API contract.

## Notes

- One-level, two-level, and three-level examples are patterns, not limits.
- For `destroy`, choose persistence assertions by model behavior:
  - `assertSoftDeleted(...)` for soft-deleting models.
  - `assertModelMissing(...)` otherwise.
- Use the app's identifier shape in assertions (`id`, `public_id`, slug, route key).
