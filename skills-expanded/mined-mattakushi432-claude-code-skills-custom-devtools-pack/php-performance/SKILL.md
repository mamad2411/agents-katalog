---
name: php-performance
description: "When to activate: PHP performance, OPcache, APCu, Redis caching, Xdebug profiling, Blackfire, autoloader optimization, composer dump-autoload, N+1 queries, PHP profiling, response time"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: php
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# PHP Performance Patterns

## When to Use

Diagnosing slow PHP request times, tuning production configuration, or deciding what to cache and where.

## Core Patterns

### OPcache: Non-Negotiable in Production

```ini
; php.ini
opcache.enable=1
opcache.enable_cli=0
opcache.memory_consumption=256
opcache.max_accelerated_files=20000
opcache.validate_timestamps=0    ; production: never re-stat files on every request
opcache.revalidate_freq=0
```

`validate_timestamps=0` means deploys must explicitly reset OPcache (`opcache_reset()` or a rolling restart) — file changes won't be picked up otherwise. This trade-off is worth it: file-timestamp checks on every request are a measurable tax at scale.

### Preloading (PHP 7.4+)

```php
// preload.php — loaded once at FPM/CLI-server startup, classes stay in shared memory
opcache_compile_file(__DIR__ . '/vendor/autoload.php');

foreach (glob(__DIR__ . '/app/Models/*.php') as $file) {
    opcache_compile_file($file);
}
```

```ini
opcache.preload=/var/www/preload.php
opcache.preload_user=www-data
```

### Autoloader Optimization

```bash
# Development: PSR-4 lookup, file-based, slower but no rebuild needed
composer dump-autoload

# Production: classmap, resolves in O(1) instead of directory scanning
composer install --no-dev --optimize-autoloader --classmap-authoritative
```

### Application-Level Caching

```php
// APCu — fast, in-process, single-server only
$value = apcu_fetch('config:feature_flags', $found);
if (!$found) {
    $value = FeatureFlags::loadFromDatabase();
    apcu_store('config:feature_flags', $value, ttl: 300);
}

// Redis — shared across servers, required once you scale beyond one box
Cache::remember('dashboard:stats:' . $userId, now()->addMinutes(5), function () use ($userId) {
    return DashboardStatsCalculator::for($userId);
});
```

Use APCu for per-process hot data that's cheap to recompute (config, feature flags); use Redis for anything that must stay consistent across multiple app servers.

### Profiling: Find Before You Fix

```bash
# Xdebug profiling (dev/staging only — heavy overhead)
php -d xdebug.mode=profile -d xdebug.output_dir=/tmp/profiles script.php

# Blackfire — low-overhead, safe to sample in production
blackfire run php artisan queue:work --once
```

Never guess at a bottleneck — profile first. The most common findings are N+1 queries (see `php-database.md`) and unbounded loops over large datasets, not raw CPU-bound PHP execution.

### Defer Heavy Work Out of the Request Path

```php
// BAD: PDF generation blocks the HTTP response for seconds
public function download(Invoice $invoice)
{
    return response()->streamDownload(fn () => $this->pdfGenerator->render($invoice));
}

// GOOD: generate async, notify when ready
GenerateInvoicePdf::dispatch($invoice->id);
return response()->json(['status' => 'processing'], 202);
```

## Checklist

- [ ] OPcache enabled with `validate_timestamps=0` in production, reset on deploy
- [ ] Autoloader built with `--optimize-autoloader --classmap-authoritative` for production installs
- [ ] Hot, cheap-to-recompute data cached in APCu; shared/cross-server data cached in Redis
- [ ] Bottlenecks identified via profiler output, not guesswork
- [ ] Slow work (PDF/report generation, bulk email, external API fan-out) moved off the request path
- [ ] N+1 queries checked (see `php-database.md`) before reaching for caching as a band-aid

## Anti-Patterns

```php
// BAD: caching a query result that's already fast, adding cache-invalidation
// complexity for no measurable win
Cache::remember('user:count', 60, fn () => User::count());

// GOOD: cache things that are actually expensive to compute or fetch —
// external API calls, complex aggregations, heavy joins
Cache::remember('analytics:cohort:' . $cohortId, now()->addHour(), function () use ($cohortId) {
    return $this->analyticsService->computeCohortRetention($cohortId);
});
```

## Quick Reference

| Symptom | First Check |
|---|---|
| Slow across all endpoints | OPcache disabled/misconfigured |
| Slow specific list/detail pages | N+1 queries — eager load |
| Slow on deploy, fast after | OPcache not reset after deploy |
| Slow external API calls | Move to a queued job, don't block the request |
| High memory on large exports | Use `chunk()`/`lazy()` instead of loading all rows |

## See Also

- `skills/php-ecosystem/php-database.md`
- `skills/php-ecosystem/php-async.md`
- `skills/php-ecosystem/composer-patterns.md`
