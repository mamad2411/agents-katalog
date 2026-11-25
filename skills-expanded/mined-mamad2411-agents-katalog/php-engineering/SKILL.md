---
name: php-engineering
description: PHP engineering guidance for PHP source, Composer manifests and lockfiles, runtime and extension discovery, PHP 8.4 implementation or migration, PHPUnit/Pest configuration, PHPStan/Psalm, PHP-CS-Fixer/PHP_CodeSniffer, PHP templates, packaging, and project quality commands. Use for ordinary PHP implementation and project mechanics; use php-design-patterns for pattern choice, php-antipatterns for smell-focused review, and php-testing-quality for test-lane work.
---

# PHP Engineering

## Use When

- Adding, changing, reviewing, testing, packaging, or refactoring `.php`, PHP templates, Composer configuration, autoloading, extensions, or PHP 8.4 migration work.
- Selecting repository-native runtime, static-analysis, formatter, and quality commands.

Do not use this as the primary skill for pattern selection, smell-only review, or test strategy; route those to the sibling PHP skills.

## Scope And Routing

Own PHP language, runtime, Composer, template-boundary, and implementation mechanics. Load [`php-design-patterns`](../php-design-patterns/SKILL.md) for positive design choices, [`php-antipatterns`](../php-antipatterns/SKILL.md) for evidence-backed smells, and [`php-testing-quality`](../php-testing-quality/SKILL.md) for tests and quality lanes.

## Workflow

1. Inspect supported PHP versions, Composer files, lockfile, extensions, autoloading, framework/template conventions, scripts, CI, and existing quality commands.
2. Preserve the target PHP compatibility range; use PHP 8.4 syntax only when the declared runtime supports it or a version-gated migration is the task.
3. Follow local namespaces, error contracts, template boundaries, and repository-native commands.
4. Run the narrowest configured syntax, static-analysis, formatter, and behavior checks that cover the changed contract.

## Runtime, Extensions, And Composer

Read `composer.json`, `composer.lock`, platform constraints, `ext-*` requirements, Composer repositories/configuration, scripts, plugins, installers, and PSR-4/classmap autoloading before changing dependencies or runtime behavior. Prefer Composer-autoloaded namespaces over manual includes. Route provenance, registry trust, lockfile integrity, and executable plugin/script review to [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md).

## Idiomatic PHP

Use `declare(strict_types=1)` when consistent with the project. Give parameters, returns, and properties explicit types; use enums and readonly/value objects where they encode real invariants; throw specific exceptions; inject dependencies through constructors at external boundaries. Preserve simple, explicit control flow and context-specific output encoding.

## PHP 8.4 Guidance

For PHP 8.4 adoption, compatibility review, or migration, load [`references/php-84-migration.md`](references/php-84-migration.md). Do not copy 8.4-only constructs into projects supporting PHP 8.3 or older without a compatible alternative or version-gated release plan.

## Web And Template Boundaries

Controllers and application services prepare typed, escaped-by-sink, localization-ready view data; templates render it. JavaScript/TypeScript crosses through a documented JSON or finite `data-*` boundary and progressively enhances. Never concatenate untrusted data into HTML, JavaScript, CSS, URLs, SQL, or shell commands.

## Errors, Resources, And I/O

Use deliberate exception boundaries, translate infrastructure errors only where the caller contract requires it, and do not suppress errors. Make files, streams, database transactions, locks, and remote resources have explicit ownership and cleanup. Bound I/O inputs, timeouts, and response sizes at their external boundary.

## Pattern Routing

Use [`php-design-patterns`](../php-design-patterns/SKILL.md) for value objects, enums, factories, interfaces, adapters, repositories, application services, presenters, middleware, and resource/transaction ownership.

## Testing Routing

Use [`php-testing-quality`](../php-testing-quality/SKILL.md) for PHPUnit, Pest, Behat, integration, browser, mutation, static-analysis, and compatibility lanes. Use [`test-driven-development`](../test-driven-development/SKILL.md) for behavior changes and [`systematic-debugging`](../systematic-debugging/SKILL.md) for active failures.

## Documentation Routing

Use [`documentation-engineering`](../documentation-engineering/SKILL.md) for PHPDoc and reader-facing documentation. Native types come first; PHPDoc records caller-relevant facts native types cannot express.

## API, Database, And Observability Routing

Use [`api-design`](../api-design/SKILL.md) for public contracts, SQL skills for database-native schema/query behavior, and [`observability-engineering`](../observability-engineering/SKILL.md) for durable telemetry design.

## Styling And JavaScript Routing

Use [`css-scss-styling`](../css-scss-styling/SKILL.md) for CSS/SCSS and [`javascript-typescript-engineering`](../javascript-typescript-engineering/SKILL.md) for JavaScript/TypeScript implementation, packages, and tooling.

## Internationalization Routing

Use [`internationalization-localization`](../internationalization-localization/SKILL.md) for message design, locale negotiation, formatting, fallback, and localization testing.

## Security And Supply-Chain Routing

Use [`security-review`](../security-review/SKILL.md) for trust boundaries: requests, sessions, CSRF, authorization, templates, uploads, paths, deserialization, SQL, outbound requests, secrets, and error disclosure. Use [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md) before trusting Composer packages, scripts, plugins, or registries.

## Anti-Patterns

Avoid weak/implicit types, dynamic property bags, global service locators, include-time effects, broad exception swallowing, error suppression, and string-built SQL/HTML/JavaScript. Use [`php-antipatterns`](../php-antipatterns/SKILL.md) for an evidence-backed refactoring review.

## Successful Use

Report the supported PHP/runtime evidence, changed language or Composer surface, selected compatibility policy, checks run, and remaining unverified host or extension assumptions.

## TypeScript Zod Interoperability

For a real TypeScript/backend JSON crossing, load [`zod-engineering`](../zod-engineering/SKILL.md). PHP still parses and validates, maps DTOs, escapes output, and converts errors safely; use shared fixtures for wire parity.
