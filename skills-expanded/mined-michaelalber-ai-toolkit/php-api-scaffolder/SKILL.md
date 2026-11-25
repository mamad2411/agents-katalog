---
name: php-api-scaffolder
audience: team
description: >
  Scaffolds Laravel API endpoints with API Resource responses, Form Request validation, Sanctum
  authentication, throttle-based rate limiting, URI versioning, OpenAPI documentation, and
  health checks. PHP analog of fastapi-scaffolder, minimal-api-scaffolder, and axum-scaffolder.
  Use when creating REST APIs in Laravel, adding API endpoints, setting up API routing and
  middleware, or configuring API infrastructure.
---

# PHP API Scaffolder (Laravel)

> "A good API is easy to use correctly and hard to use incorrectly."
> -- Joshua Bloch

> "Be conservative in what you send, be liberal in what you accept."
> -- Postel's Law

## Core Philosophy

This skill scaffolds **production-grade Laravel API endpoints** — not just a route and a closure. Every
endpoint ships with input validation (Form Request), output shaping (API Resource), authentication
(Sanctum), rate limiting (throttle), a version prefix, a documented OpenAPI contract, and a consistent
error envelope. The default is `routes/api.php` with the `api` middleware group, which is stateless and
already namespaced under `/api`.

The endpoint is a boundary. Untrusted input is validated and typed before it reaches any service; output
is shaped through a Resource so schema and sensitive columns never leak. Errors return a predictable JSON
shape with the correct HTTP status — `422` for validation, `401`/`403` for auth, `429` for throttling.

**Non-Negotiable Constraints:**
1. **`declare(strict_types=1)`** in every generated PHP file
2. **Form Request validation** on every write endpoint — never raw `$request->input()`
3. **API Resource** on every response — never return Eloquent models or arrays directly
4. **Versioned URIs** — `/api/v1/...`; breaking changes bump the version, never mutate `v1`
5. **Auth + throttle middleware** declared on every non-public route
6. **OpenAPI annotations** kept next to the controller action they describe

The full domain-principle set, knowledge-base lookups, AI discipline rules, anti-patterns, and
error-recovery procedures live in `references/api-conventions.md`.

## Workflow

### Phase 1: DETECT

```bash
php -v | head -1
grep -E '"(php|laravel/framework)"' composer.json
# Does an API route file / Sanctum exist yet?
ls routes/api.php 2>/dev/null && grep -rn "Sanctum\|auth:sanctum" routes/ app/ | head
# Existing version prefixes and limiters
grep -rn "prefix('v" routes/ ; grep -rn "RateLimiter::for" app/
```

If `routes/api.php` is absent on Laravel 11-13, run `php artisan install:api` (installs Sanctum, creates
the file). Record version, whether Sanctum is present, existing limiters, and the OpenAPI tool in use
(`l5-swagger`, `scribe`, or none).

### Phase 2: SCAFFOLD

See `references/route-template.md` for full controller, request, resource, and route content, and
`references/security-patterns.md` for auth, throttle, CORS, and the error envelope.

```
app/Http/Controllers/Api/V1/<Name>Controller.php   # OpenAPI annotations + thin actions
app/Http/Requests/Api/V1/Store<Name>Request.php
app/Http/Resources/V1/<Name>Resource.php
routes/api.php                                       # v1 group: auth + throttle
app/Providers/AppServiceProvider.php / RouteServiceProvider  # RateLimiter::for('api', ...)
tests/Feature/Api/V1/<Name>EndpointTest.php
```

### Phase 3: SECURE & DOCUMENT

```php
// routes/api.php
Route::get('/health', HealthController::class);     // public liveness

Route::prefix('v1')->middleware(['auth:sanctum', 'throttle:api'])->group(function (): void {
    Route::apiResource('users', UserController::class);
});
```

Generate the spec: `php artisan l5-swagger:generate` (or `php artisan scribe:generate`).

### Phase 4: VERIFY

```bash
php artisan route:list --path=api
vendor/bin/pest tests/Feature/Api          # or phpunit
vendor/bin/pint --dirty                    # Laravel's default style fixer (wraps php-cs-fixer)
curl -s localhost:8000/api/health          # {"status":"ok"}
# 429 after exceeding the limiter; 422 on bad input; 401 without a token
```

## State Block

```xml
<php-api-scaffolder-state>
  phase: DETECT | SCAFFOLD | SECURE | VERIFY | COMPLETE
  endpoint: [resource name]
  laravel_version: [detected]
  api_version: v1
  sanctum_installed: true | false
  throttle_configured: true | false
  openapi_tool: l5-swagger | scribe | none
  resource_created: true | false
  request_created: true | false
  tests_scaffolded: true | false
  last_action: [description]
</php-api-scaffolder-state>
```

## Output Template

### Laravel API Endpoint Scaffold: [Endpoint Name]

```markdown
## API Endpoint Scaffold: [Endpoint Name]

### Files Created
- [ ] `app/Http/Controllers/Api/V1/<Name>Controller.php` (OpenAPI annotated)
- [ ] `app/Http/Requests/Api/V1/Store<Name>Request.php`
- [ ] `app/Http/Resources/V1/<Name>Resource.php`
- [ ] `tests/Feature/Api/V1/<Name>EndpointTest.php`

### Routing & Middleware
- [ ] Registered under `Route::prefix('v1')`
- [ ] `auth:sanctum` applied (or documented as public)
- [ ] `throttle:api` applied; limiter defined
- [ ] Health route `GET /api/health` present

### Contract
- [ ] OpenAPI annotations on each action
- [ ] Spec regenerated (`l5-swagger:generate` / `scribe:generate`)
- [ ] Error envelope consistent (422 / 401 / 403 / 429)

### Verification
- [ ] `route:list` shows versioned routes
- [ ] Feature tests green (happy path + 422 + 401 + 429)
- [ ] `pint --dirty` clean
```

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `php-feature-slice` | Provides the feature folder + service layer the controller delegates to. Use together for a full slice with production endpoints. |
| `php-security-review` | Audit the new endpoints for OWASP API risks (authz, mass assignment, rate limits) after scaffolding. |
| `php-migration-manager` | When an endpoint needs new tables/columns, manage the migration lifecycle. |
| `php-package-scaffold` | When the API client/SDK is published as a Composer package. |
| `tdd-loop` | Drive each endpoint test-first (request → 422/401/200) before generating the action. |
