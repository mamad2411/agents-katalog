---
name: php-feature-slice
audience: team
description: >
  Scaffolds feature-based PHP / Laravel architecture using feature folders, thin controllers,
  Form Requests, a service/action layer, and API Resources. PHP analog of dotnet-vertical-slice
  and python-feature-slice — no mediator library; uses the Laravel service container for
  dependency injection and structural CQRS conventions. Use when creating feature-based PHP
  projects, adding Laravel features, scaffolding service layers, or organizing PHP code by
  feature rather than by technical layer.
---

# PHP Feature Slice Architecture

> "The best code is code that never has to be written."
> -- Jeff Atwood

> "Organize around business capabilities, not technical layers."
> -- Sam Newman, *Building Microservices*

## Core Philosophy

Feature slice architecture organizes code by business capability, not by technical layer. Laravel's default skeleton is layer-based — `app/Http/Controllers`, `app/Models`, `app/Services` spread one feature across many directories. This skill replaces that with self-contained vertical slices: `app/Features/Orders/`, `app/Features/Users/`, each owning its full stack — controller, Form Request, service, API Resource, and tests.

In PHP with Laravel, the mediator pattern (FreeMediator in .NET) is replaced by Laravel's **service container**. Service classes are constructor-injected into controllers; the container resolves them automatically. CQRS separation is a structural and naming convention — `OrderReadService` vs `OrderWriteService` — not a library contract.

**Non-Negotiable Constraints:**
1. **`declare(strict_types=1)`** at the top of every PHP file
2. **Feature isolation** — no cross-feature imports; features communicate through shared domain code only
3. **Service layer owns business logic** — controllers are thin; no business logic in controllers
4. **Form Requests for all input** — never trust raw `$request->input()`; validation lives in `FormRequest::rules()`
5. **API Resources for all output** — never return Eloquent models directly from controllers
6. **Eloquent or bound parameters only** — never string-concatenated SQL

**What this skill is NOT:**
- It is NOT a microservices guide — feature slices live within a single Laravel application
- It is NOT prescriptive about feature count — start with the features you have
- It is NOT a replacement for DDD — it is compatible with DDD but does not require it

The 10 domain principles (Feature Isolation, Service Autonomy, Minimal Abstractions, DI via the
Container, Read/Write Separation, Validation at the Boundary, Explicit Output Shaping, Controller
Thinness, Strict Typing, Test Proximity) and the grounding `search_knowledge` query map live in
`references/domain-principles.md`. CQRS naming conventions live in `references/laravel-cqrs-conventions.md`.

## Workflow

### Phase 1: DETECT

**Objective:** Understand the existing structure before scaffolding.

```bash
# PHP and Laravel version
php -v | head -1
grep -E '"(php|laravel/framework)"' composer.json

# Existing structure — layered, modular, or already feature-based
find app -type d -not -path '*/vendor/*' | head -30

# Existing route registration and service bindings
grep -rn "Route::" routes/ | head -20
grep -rn "->bind\|->singleton" app/Providers/ | head -20
```

Record: PHP version, Laravel version (5.5 / 6.x / 8+ / 12.x), current layout, route file (`routes/api.php` vs `web.php`), auth pattern.

### Phase 2: SCAFFOLD

Create the feature namespace. See `references/feature-folder-template.md` for file-by-file content.

```
app/Features/<Name>/
  Controllers/<Name>Controller.php   # thin; resolve → call service → resource
  Requests/Store<Name>Request.php     # FormRequest: rules() + toDto()
  Requests/Update<Name>Request.php
  Services/<Name>ReadService.php       # queries
  Services/<Name>WriteService.php      # commands
  Resources/<Name>Resource.php         # JsonResource output shaping
  Dtos/Create<Name>Dto.php             # validated, readonly transfer object
routes/features/<name>.php             # route group for the slice
tests/Feature/<Name>/Create<Name>Test.php
tests/Unit/<Name>/<Name>WriteServiceTest.php
```

### Phase 3: REGISTER

Wire the slice into routing and (only if an interface exists) the container.

```php
// routes/api.php
require __DIR__ . '/features/orders.php';

// app/Providers/AppServiceProvider.php — only when an interface is introduced
$this->app->bind(OrderWriteContract::class, OrderWriteService::class);
```

### Phase 4: VERIFY

```bash
php artisan route:list --path=api/v1/<name>     # routes registered
vendor/bin/pest tests/Feature/<Name> tests/Unit/<Name>   # or phpunit
vendor/bin/pint --dirty                          # Laravel's default style fixer (wraps php-cs-fixer)
# Cross-feature import check — should print nothing
grep -rn "use App\\\\Features\\\\" app/Features/<Name> | grep -v "App\\\\Features\\\\<Name>"
```

## State Block

```xml
<php-feature-slice-state>
  phase: DETECT | SCAFFOLD | REGISTER | VERIFY | COMPLETE
  feature_name: [name]
  laravel_version: [detected]
  existing_structure: layered | modular | feature-based | unknown
  routes_registered: true | false
  read_service_created: true | false
  write_service_created: true | false
  tests_scaffolded: true | false
  last_action: [description]
  next_action: [description]
</php-feature-slice-state>
```

## Output Template

### Feature Slice Scaffold: [Feature Name]

```markdown
## Feature Slice Scaffold: [Feature Name]

### Files Created
- [ ] `app/Features/<Name>/Controllers/<Name>Controller.php`
- [ ] `app/Features/<Name>/Requests/Store<Name>Request.php`
- [ ] `app/Features/<Name>/Requests/Update<Name>Request.php`
- [ ] `app/Features/<Name>/Services/<Name>ReadService.php`
- [ ] `app/Features/<Name>/Services/<Name>WriteService.php`
- [ ] `app/Features/<Name>/Resources/<Name>Resource.php`
- [ ] `app/Features/<Name>/Dtos/Create<Name>Dto.php`
- [ ] `routes/features/<name>.php`
- [ ] `tests/Feature/<Name>/Create<Name>Test.php`
- [ ] `tests/Unit/<Name>/<Name>WriteServiceTest.php`

### Registration
- [ ] Route group required into `routes/api.php`
- [ ] Prefix set: `/api/v1/<name>`; middleware: `['api', 'auth:sanctum']`

### Verification
- [ ] `php artisan route:list` shows the new routes
- [ ] `pest` / `phpunit` green for the slice
- [ ] `pint --dirty` clean
- [ ] No cross-feature imports detected
```

The feature folder diagram is in `references/domain-principles.md`. The AI discipline rules
(no-logic-in-controllers, Form Request + DTO boundary, no cross-feature imports), the 10-row
anti-patterns table, and the error-recovery procedures (cross-feature import, oversized service,
oversized controller) live in `references/discipline-and-recovery.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `php-api-scaffolder` | Endpoint-level quality (Sanctum auth, throttle, versioning, OpenAPI). Use together when a new slice needs production-grade endpoints. |
| `php-migration-manager` | When a slice needs schema changes, manage the Laravel migration lifecycle and rollback safety. |
| `php-security-review` | After scaffolding, audit the slice's validation, authorization, and query safety against OWASP. |
| `php-architecture-checklist` | Architecture quality gate. Run after several slices to verify isolation and coupling. |
| `tdd-loop` | Drive each service method test-first (RED → GREEN → REFACTOR) rather than scaffolding code ahead of tests. |
