---
name: follow-lang-php
description: Develop PHP projects with PSR standards and modern best practices
argument-hint: "[scope|setup-project]"
related:
  - follow-lang-javascript
  - follow-architecture
  - follow-my-techstack
  - follow-secret-manager
  - follow-default-config
  - follow-best-practice
  - refactor
  - setup-cicd
  - use-scripts
  - deep-research
---

## Goal

Develop PHP applications following PSR standards and modern best practices

## Scope

For PHP projects, vanilla and framework (Laravel/Symfony/Slim). Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/setup-project/SKILL.md` (argument `setup-project` — first-time Composer/PSR-4 scaffold); verify the current PHP major version and feature set via `/deep-research` at use time (official docs: https://www.php.net/, PSRs: https://www.php-fig.org/psr/)

## Execute

### 1. Check Version And Setup

> Goal: install PHP, Composer, and dev tools with live-checked versions

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest stable PHP, current PHP practices, and which language features are safe to use for the project's platform version
2. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): PHP+Composer install, `composer init` with `require.php`, PSR-4 autoload, layout, quality dev deps, verify
3. Tool inventory (runtime, Composer, analyzers, fixers, runners, Xdebug) → `references/toolchain.md`
4. Pick the framework (Laravel, Symfony, Slim) only when the project needs one — confirm with `/follow-my-techstack`

### 2. Configuration

> Goal: configure composer.json, autoload, static analysis, and code style

1. `composer.json`: `require.php`, PSR-4 `autoload` (`"Vendor\\Package\\": "src/"`) and `autoload-dev` for tests — concrete new-project steps in `workflows/setup-project/SKILL.md`
2. `phpstan.neon` (`level: 8` for new code, `paths: [src]`) and `.php-cs-fixer.php` (`@PSR12`) with overrides only per `/follow-default-config`
3. Set `php.ini` per environment: dev `display_errors = On`, `error_reporting = E_ALL`; prod `display_errors = Off`

### 3. Project Structure

> Goal: organize directories per PSR-4 autoloading

1. `src/` for source, `tests/` for tests, `config/` for configuration
2. Namespace layout mirrors `src/` exactly (PSR-4)
3. Use Clean Architecture or MVC per `/follow-architecture`

### 4. Code Standards

> Goal: write PSR-12-compliant, fully typed PHP

1. `declare(strict_types=1);` in every file; type hints and return types on every function; typed properties
2. PSR-12: LF endings, file ends with single LF, omit closing `?>`, 4-space indent (no tabs), soft limit 120 chars, lowercase reserved keywords, short type keywords (`bool`, `int`)
3. Namespaces per PSR-4; classes `PascalCase`, methods `camelCase`/`studlyCaps` per PSR-1, functions `snake_case` where not class-bound
4. Use modern features available on the platform version (enums, readonly, `#[\Override]`, property hooks, pipe operator, `#[\NoDiscard]`) — live-check availability, never target features above `require.php`

### 5. Dependency Management

> Goal: manage dependencies and wiring cleanly

1. Composer for dependencies; commit `composer.lock`, never float ranges in `require`
2. Use a DI container (PSR-11) and constructor injection; interfaces for abstraction; service providers on Laravel/Symfony
3. Avoid global state

### 6. Testing And Quality

> Goal: keep the codebase analyzed, styled, and tested

1. PHPUnit (or Pest for modern syntax) — `vendor/bin/phpunit`; mock external dependencies
2. `vendor/bin/phpstan analyse src` and `vendor/bin/php-cs-fixer fix` in CI before merge
3. Add Psalm for deeper analysis if the codebase warrants it; run `/setup-cicd` for automated checks

## Rules

### 1. PSR Standards

- PSR-4 autoloading, PSR-12 coding style, PSR-3 logging interface, PSR-7 HTTP messages, PSR-11 container — adopt the interface, not a bespoke one

### 2. Type Safety

- `declare(strict_types=1);` everywhere; full parameter/return/property types; union types and enums where they clarify

### 3. Security

- Validate input, escape output, prepared statements, `password_hash()`, HTTPS, proper file permissions, secrets via env (`/follow-secret-manager`)

### 4. Performance

- OPcache in production; avoid N+1 queries; cache expensive results; async processing for long tasks; HTTP/2 + compression

### 5. Documentation

- PHPDoc on classes/methods/properties with `@param`, `@return`, `@throws`; README.md and CHANGELOG.md maintained

### 6. No Stale Pins

- Never restate PHP version numbers or feature timelines from memory; live-check via `/deep-research` at use time

- Use /follow-lang-javascript if needed
- Use /follow-best-practice if needed
- Use /refactor if needed
- Use /setup-cicd if needed
- Use /use-scripts if needed

## Expected Outcome

- PHP project compliant with PSR standards
- High type safety with strict types everywhere
- Passing static analysis (PHPStan level 8), consistent code style, and covering tests
- Secure and performant production setup
