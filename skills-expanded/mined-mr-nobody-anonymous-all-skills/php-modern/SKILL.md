---
name: php-modern
description: "Write modern PHP 8: typed properties, enums, readonly classes, PSR-4 autoloading, Composer dependency hygiene, PSR-12 style and PHPUnit testing."
type: procedural
category: programming
domain: programming
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - modern php 8 patterns
  - php enum refactor
  - composer dependency conflict
  - psr-12 code review
  - phpunit test setup
keywords:
  - php
  - composer
  - psr-4
  - phpunit
  - enum
  - readonly
source: custom
enabled: true
---

# Modern PHP 8

## Purpose

Write modern PHP 8: typed properties, enums, readonly classes, PSR-4 autoloading, Composer dependency hygiene, PSR-12 style and PHPUnit testing.

## When to Use

- You are adding or refactoring PHP application code targeting PHP 8.1 or newer.
- A Composer dependency conflict or autoload failure needs a minimal, explainable fix.
- Legacy code must be modernized incrementally without breaking public behaviour.

## When NOT to Use

- The runtime is still PHP 7.x and cannot be upgraded; the API surface differs substantially.
- The task is WordPress theme CSS or front-end-only work with no PHP logic.
- You need a framework-specific decision (Laravel, Symfony) that should follow that framework's own conventions.

## Capabilities

- Apply strict typing, enums and readonly value objects without breaking callers.
- Resolve Composer conflicts by reasoning about version constraints rather than deleting locks.
- Set up PSR-4 autoloading, static analysis (PHPStan) and PHPUnit coverage for changed code.
- Refactor legacy code behind tests, in reviewable slices.

## Inputs

- The PHP version constraint from composer.json and the framework in use, if any.
- The failing test or the code path being changed, plus its public callers.
- The project's style and static-analysis baseline configuration.

## Workflow

1. Read composer.json and the CI config to learn the supported PHP range and existing tooling.
2. Write or extend a PHPUnit test that captures current behaviour before refactoring.
3. Refactor toward typed signatures, enums and readonly properties in small, reviewable commits.
4. Run the project's own gates: PHPStan/Psalm, PHP-CS-Fixer, PHPUnit.
5. Update composer constraints only with a `composer update --dry-run` diff to justify the change.

## Tools

- composer
- phpunit
- phpstan / psalm
- php-cs-fixer

## Examples

- `composer update --dry-run --with-dependencies`
- `vendor/bin/phpunit --filter ShopTest`
- `vendor/bin/phpstan analyse src --level=max`

## Safety

- Never delete composer.lock to silence a conflict; that makes builds non-reproducible.
- Dynamic property changes break serialization and public payloads; migrate callers in the same change.
- Do not widen PHP version support without verifying CI runs the new version.

## Source

All-Skills canonical library (`skills/programming/php-modern`). First-party skill, maintained in this repository.

## Notes

- Enums replace string constants but change serialization; check database and API encodings first.
- `declare(strict_types=1)` at file scope is the cheapest correctness win.
- Pairs with: `programming/python-idiomatic-style`, `development/code-review`.
