# Laravel Framework Fundamentals

## Summary

**One-sentence:** Use Laravel's framework idioms correctly: service container, routing/controller resolution, middleware pipeline, providers, facades vs DI, and config caching.

**One-paragraph:** Laravel offers many ways to do the same thing — facades, helpers, service container, providers, contracts. Pick the idiomatic one: constructor-inject contracts, register bindings in providers, define routes in route files, use middleware for cross-cutting concerns, cache config + routes in production. Mixing facades into service classes makes testing hard; ignoring providers leads to bootstrap-time bugs.

**Ефективно для:**

- Greenfield Laravel сервіси — задати ідіоматичну архітектуру з самого початку.
- Refactor legacy Laravel де facades всюди + бізнес-логіка в Route::get callbacks.
- Setup performance optimizations: route:cache + config:cache + opcache + composer optimization.
- Сервіс-контейнер сейлс: contract → impl, binding в service provider.

## Applies If (ALL must hold)

- Laravel 10/11/12 project (recent framework versions).
- Application has services + dependencies (not a 5-route prototype).
- Production deployment needs `php artisan route:cache` + `config:cache`.
- Tests must run without booting Laravel (unit tests).

## Skip If (ANY kills it)

- Project standardizes on Lumen (micro-framework subset) — different lifecycle.
- Tiny single-file artisan app.
- Already DDD/Hexagonal architecture with Laravel as IoC only — different methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service contract | PHP interface | domain model |
| Implementation class | PHP class implementing the contract | developer |
| Environment vars | .env file | ops |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: contract-bind-in-provider, constructor-injection-over-facades, routes-in-route-files-only, config-via-config-helper, middleware-for-crosscutting | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `create-contract-and-binding` | sonnet | Templated interface + provider. |
| `design-middleware-boundary` | opus | Decide which concerns are cross-cutting. |
| `lint-facades-in-services` | haiku | Mechanical grep. |

## Templates

| File | Purpose |
|------|---------|
| `templates/PaymentServiceProvider.php` | Service Provider binding contracts to implementations |
| `templates/config-stripe.php` | Config file pattern that survives config:cache |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-php-laravel.py` | Validate the Laravel module artefact against the schema | Pre-commit + CI |

## Related

- [[php-laravel-patterns]]
- [[php-laravel-queues]]
- [[php-eloquent]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, stack, runtime, scale, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/PaymentServiceProvider.php`

```php
<?php

namespace App\Providers;

use App\Contracts\MailService;
use App\Contracts\CacheService;
use App\Services\SendgridMailService;
use App\Services\RedisCacheService;
use Illuminate\Support\ServiceProvider;

class PaymentServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->bind(MailService::class, SendgridMailService::class);
        $this->app->bind(CacheService::class, RedisCacheService::class);
    }

    public function boot(): void
    {
        // Macros, route model bindings, blade directives go here — not env() or DB queries.
    }
}
```

### `templates/config-stripe.php`

```php
<?php

return [
    'key' => env('STRIPE_KEY'),
    'secret' => env('STRIPE_SECRET'),
    'webhook_secret' => env('STRIPE_WEBHOOK_SECRET'),
    'currency' => env('STRIPE_CURRENCY', 'USD'),
    'capture_method' => env('STRIPE_CAPTURE_METHOD', 'automatic'),
];
```
