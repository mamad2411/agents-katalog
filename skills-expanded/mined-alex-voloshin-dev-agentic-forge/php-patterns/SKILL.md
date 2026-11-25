---
name: php-patterns
description: PHP stack conventions agentic-forge applies when the detected stack is PHP — the toolchain (composer, PHPUnit, PHPStan/Psalm, PHP-CS-Fixer), strict-types and PSR idioms, testing discipline, layout, and the high-value PHP pitfalls (incl. SQL injection). Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# PHP patterns

The PHP stack pack: loaded by the `software-engineer` / `qa-engineer` roles (and the
`code-review` lint aspect) when `stacks.detect` reports PHP. It carries only what is
**PHP-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md).
(Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's composer scripts** (`composer.json` `scripts`) and CI. Defaults:

| Job | Conventional command | Gate |
| --- | --- | --- |
| test | `composer test` (or `vendor/bin/phpunit`) | green; new behaviour covered |
| static analysis | `vendor/bin/phpstan analyse` (or `psalm`) | clean at the repo's level |
| format/lint | `vendor/bin/php-cs-fixer fix` (or `phpcs`, PSR-12) | applied |

Run PHPStan/Psalm and PHP-CS-Fixer on the change before declaring done; never silence a checker
(no new baseline entries or `@phpstan-ignore`) — fix the cause or justify it in the diff.

## Idioms

- **`declare(strict_types=1)`** as the first statement of every file (directly after `<?php`);
  **type declarations** on params, returns, and properties. Follow **PSR-12** style and **PSR-4**
  autoloading (via Composer).
- Modern PHP (8.1+): **constructor property promotion**, **enums**, **readonly** properties,
  the **`match`** expression, named arguments, null-safe **`?->`**.
- **Parameterised queries** (PDO prepared statements) — never build SQL by string concatenation;
  validate `$_GET`/`$_POST`/external input at the boundary.

## Testing

- **PHPUnit** with **data providers** for case tables; mock at boundaries. Cover the happy path
  plus a boundary and an **exception** case. Deterministic — no real network/clock; never weaken
  or delete a test to go green.

## Pitfalls (PHP-specific, high-value)

- **SQL injection** — string-built queries; always use prepared statements with bound params.
- **Loose `==`** / type juggling (`0 == "a"` quirks across versions) — use **`===`**; not
  declaring `strict_types`.
- **Unvalidated superglobals** (`$_GET`/`$_POST`/`$_REQUEST`); swallowed exceptions; global
  state; **`null` handling** without the null-safe operator.

## Definition of done (PHP)

PHPStan/Psalm clean at the repo's level, PHPUnit green with the new boundary/exception cases,
PHP-CS-Fixer / PSR-12 applied, `declare(strict_types=1)` present, queries parameterised, external
input validated — using the repo's own composer scripts where declared.
