---
name: composer-patterns
description: "When to activate: Composer, composer.json, composer.lock, PSR-4 autoloading, semantic versioning constraints, dev dependencies, composer audit, private package repositories, PHP dependency management"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: php
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Composer Patterns

## When to Use

Setting up a PHP project's dependencies, authoring a library's `composer.json`, resolving version conflicts, or auditing dependencies for known vulnerabilities.

## Core Patterns

### composer.json Structure

```json
{
    "name": "acme/billing",
    "description": "Billing domain package",
    "type": "library",
    "require": {
        "php": "^8.2",
        "ramsey/uuid": "^4.7"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.5",
        "phpstan/phpstan": "^1.10"
    },
    "autoload": {
        "psr-4": { "Acme\\Billing\\": "src/" }
    },
    "autoload-dev": {
        "psr-4": { "Acme\\Billing\\Tests\\": "tests/" }
    },
    "minimum-stability": "stable",
    "prefer-stable": true
}
```

### Version Constraints

```
"laravel/framework": "^10.0"   // allows 10.x, blocks 11.0 — caret = safe minor/patch updates
"symfony/console": "~6.3.0"    // allows 6.3.x only — tilde pins the last segment
"vendor/pkg": "10.4.2"         // exact pin — only when you must freeze a specific release
```

Prefer `^` for applications; use exact pins only for packages known to break on minor bumps.

### PSR-4 Autoloading

```json
"autoload": {
    "psr-4": {
        "App\\": "app/",
        "Acme\\Shared\\": "packages/shared/src/"
    }
}
```

Namespace `App\Services\OrderService` maps to `app/Services/OrderService.php`. Run `composer dump-autoload -o` after adding new namespaces or before a production deploy to generate the classmap (faster than PSR-4 lookup at runtime).

### Lockfile Discipline

```bash
# Install exactly what's in composer.lock — use in CI and production
composer install --no-dev --optimize-autoloader

# Update dependencies and regenerate the lockfile — local dev only
composer update

# Update a single package without touching the rest of the lock
composer update vendor/package --with-dependencies
```

Always commit `composer.lock` for applications (guarantees reproducible installs). Library packages typically `.gitignore` their own lockfile since consumers resolve versions themselves.

### Dev-Only Dependencies

```bash
composer require --dev phpunit/phpunit phpstan/phpstan friendsofphp/php-cs-fixer
```

Anything only needed for testing, static analysis, or local tooling belongs in `require-dev` — keeps production installs (`--no-dev`) smaller and reduces the deployed attack surface.

### Vulnerability Scanning

```bash
composer audit
```

Run in CI on every PR; fail the build on any advisory with severity `high` or above. Combine with Dependabot/Renovate for automated update PRs.

### Private Package Repositories

```json
"repositories": [
    { "type": "composer", "url": "https://packages.example.com" },
    { "type": "vcs", "url": "git@github.com:acme/internal-lib.git" }
],
"require": {
    "acme/internal-lib": "^2.0"
}
```

Store repository credentials in `auth.json` (git-ignored), never inline in `composer.json`.

## Checklist

- [ ] `composer.lock` committed for applications
- [ ] `require-dev` used for test/lint/analysis-only packages
- [ ] `composer audit` runs in CI and gates the build
- [ ] Version constraints use `^` unless a specific package is known to break on minors
- [ ] `composer dump-autoload -o` (or `--classmap-authoritative`) run as part of the production build
- [ ] No credentials committed inside `composer.json` — use `auth.json` or environment variables

## Anti-Patterns

```json
// BAD: unconstrained wildcard — any future major version can break the app silently
"require": { "guzzlehttp/guzzle": "*" }

// GOOD: bounded to a known-compatible major line
"require": { "guzzlehttp/guzzle": "^7.8" }
```

## Quick Reference

| Task | Command |
|---|---|
| Reproducible install (CI/prod) | `composer install --no-dev --optimize-autoloader` |
| Add a runtime dependency | `composer require vendor/package` |
| Add a dev-only dependency | `composer require --dev vendor/package` |
| Check for known vulnerabilities | `composer audit` |
| Regenerate optimized autoloader | `composer dump-autoload -o` |
| See why a version is pinned | `composer why vendor/package` |

## See Also

- `skills/php-ecosystem/php-patterns.md`
- `skills/php-ecosystem/php-performance.md`
