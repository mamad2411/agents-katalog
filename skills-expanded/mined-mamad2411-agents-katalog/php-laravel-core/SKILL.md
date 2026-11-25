---
name: php-laravel-core
description: "Shared reference for the Laravel cluster: the layered request flow (controller → service → action → model), typed Eloquent + Form Request validation, the standard JSON response envelope, the test/CI matrix, and the version/tooling baseline. USE WHEN structuring controllers, writing validation, wiring the test/verify pipeline, or choosing tooling — the conventions every Laravel spoke shares."
cluster: php-laravel
version: 1.0.0
---

# PHP / Laravel Core

Shared model for the `php-laravel` cluster. The patterns, TDD, verification, and security spokes
all lean on these conventions — keep them consistent here so no spoke contradicts another.

## 1. The decision this cluster turns on: thin controllers, layered flow

Every request crosses the **same one-way pipeline**. Each layer has exactly one job, and logic
flows down, never back up:

```
HTTP Request ─> Route (model-bound) ─> Form Request (validate + authorize)
            ─> Controller (thin: translate I/O) ─> Service (orchestrate)
            ─> Action (single use case) ─> Model / Repository (persist)
            ─> API Resource (shape) ─> JSON envelope
```

- **Controller** — thin. Receives the validated request, calls one service/action, returns a
  resource. No business logic, no queries. → `laravel-patterns`
- **Service** — coordinates a multi-step use case across actions/models.
- **Action** — a single-purpose use case (`CreateOrderAction::handle()`); the smallest reusable unit.
- **Model** — typed: `$fillable`, `$casts` (enums/value objects), named scopes; never `unguard()`.
- **Form Request** — the *only* place inputs are validated and authorization is asserted
  (`authorize()` + `rules()`); transform to a DTO before passing inward. → `laravel-security`

**Rule:** if logic lives in a controller, it's in the wrong place. Push it down one layer.

## 2. Validation & the trust boundary

The HTTP request is **untrusted**. Nothing reaches a service un-validated.

- Validate in **Form Requests** (`rules()`), authorize in the same class (`authorize()` via a
  policy/gate). Never derive privileged fields from the raw payload.
- Mass-assignment is guarded by `$fillable`; prefer DTOs/explicit mapping over `Model::unguard()`.
- Output is escaped by Blade (`{{ }}`); queries use Eloquent/binding, never string-built SQL.
- Full hardening surface (CSRF, uploads, rate limiting, signed URLs, headers, CORS) → `laravel-security`.

## 3. Standard JSON response envelope

Every API response — success or error — uses the same four-key shape so clients (and tests)
can rely on it:

```php
return response()->json([
    'success' => true,
    'data'    => OrderResource::make($order), // or ::collection(...) for lists
    'error'   => null,
    'meta'    => null,                          // pagination block on lists
], 201);
```

Tests assert this with `assertJsonStructure(['success', 'data', 'error', 'meta'])`. Lists put
`page`/`per_page`/`total` under `meta`. → `laravel-patterns` (resources), `laravel-tdd` (assertions).

## 4. Test layers & database strategy

| Layer | Covers | Tool |
|---|---|---|
| **Unit** | pure PHP: value objects, services, actions | Pest / PHPUnit |
| **Feature** | HTTP, auth, validation, response envelope | `actingAs` + JSON asserts |
| **Integration** | DB + queue + external boundaries together | `RefreshDatabase` + fakes |

- Default to **Pest** for new tests; use PHPUnit only if the project already standardizes on it.
- **`RefreshDatabase`** is the default DB trait (migrate once, transaction per test on supported
  drivers); use `DatabaseTransactions` when the schema is already migrated.
- Isolate side effects with fakes: `Bus::fake()`, `Queue::fake()`, `Mail::fake()`,
  `Notification::fake()`, `Http::fake()`. Target **80%+** coverage (unit + feature). → `laravel-tdd`

## 5. The verification gate (sequential)

Phases run in order; an earlier failure blocks the rest. This is the contract `laravel-verification`
enforces before any PR or deploy:

```
env (php/composer/artisan)  ─>  composer validate + dump-autoload
  ─>  pint --test + phpstan analyse           # lint/static must be clean
  ─>  php artisan test (+ --coverage in CI)
  ─>  composer audit                          # dependency CVEs
  ─>  migrate --pretend / migrate:status      # review destructive/irreversible
  ─>  config|route|view:cache + queue/scheduler readiness
```

→ `laravel-verification` for the full phase list and commands.

## 6. Version / tooling matrix

| Concern | Baseline | Spoke |
|---|---|---|
| Framework | Laravel 11/12 (target the project's version) | `laravel-patterns` |
| Language | PHP 8.2+ (typed props, enums, readonly) | — |
| API auth | Laravel Sanctum (Passport for OAuth) | `laravel-security` |
| Tests | Pest (default) / PHPUnit | `laravel-tdd` |
| Lint / static | Laravel Pint + PHPStan (or Psalm) | `laravel-verification` |
| Deps audit | `composer audit` | `laravel-verification` |
| Package vetting | LaraPlugins.io MCP (health + compat) | `laravel-plugin-discovery` |

## 7. Shared guardrails

- **Thin controllers**: business logic lives in services/actions, never the controller or route.
- **Validate everything** in a Form Request; the HTTP payload is untrusted; never derive
  privileged fields from it.
- **Default-deny authorization**: policies/gates + `$fillable`; never `unguard()`; scoped route
  bindings to prevent cross-tenant access.
- **Stable envelope**: every API response is `{ success, data, error, meta }`.
- **Sequential gate**: env/composer failures stop the pipeline; lint clean before tests; security
  + migration review precede release steps.
- State every widening (mass-assignment field, CORS origin, rate-limit, scope) explicitly — it's
  a security change.
