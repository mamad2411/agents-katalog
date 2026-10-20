---
name: ci-cd-php
description: "Applies when creating or modifying CI/CD pipelines for PHP projects. Covers composer caching, phpunit coverage, phpstan/psalm analysis, and composer audit."
---

# PHP CI/CD

## Setup and caching

Use `shivammathur/setup-php@v2`:

```yaml
- uses: shivammathur/setup-php@v2
  with:
    php-version: '8.3'
    extensions: mbstring, pdo_mysql
    coverage: pcov           # faster than xdebug for coverage-only
    tools: composer, phpstan, php-cs-fixer
```

Cache composer dependencies:

```yaml
- uses: actions/cache@v4
  with:
    path: vendor
    key: composer-${{ runner.os }}-${{ hashFiles('composer.lock') }}
    restore-keys: composer-${{ runner.os }}-
```

## Install (frozen)

```bash
composer install --no-interaction --prefer-dist --no-progress
```

## Coverage

```bash
phpunit --coverage-clover=coverage.xml
```

Coverage driver: `pcov` (fast, line coverage) or `xdebug` (feature-complete, slower). Use `pcov` in CI.

## Linting and static analysis

```bash
phpstan analyse src/ --level=max
# or: psalm --show-info=true
php-cs-fixer fix --dry-run --diff
```

## Dependency audit

```bash
composer audit
```

## PHP-specific gotchas

1. Use `pcov` over `xdebug` for CI coverage — it's 2-5x faster and produces identical line coverage.
2. Set `memory_limit=-1` in CI to avoid OOM on large codebases with PHPStan.
3. Cache `vendor/` (not just the composer cache dir) for faster installs when lockfile is unchanged.
4. Use `--prefer-dist` to download pre-built archives instead of cloning git repos.
5. Set `COMPOSER_NO_INTERACTION=1` environment variable as a safety net.

## Sources

- https://github.com/shivammathur/setup-php
- https://phpstan.org/user-guide/getting-started
