---
name: php-testing-quality
description: PHP testing and quality-lane guidance. Use when selecting, adding, running, or reviewing PHPUnit, Pest, Behat, PHPStan, Psalm, PHP_CodeSniffer, PHP-CS-Fixer, Infection, framework harnesses, PHP integration tests, browser E2E tests, or PHP 8.4 compatibility tests. Do not use for ordinary PHP implementation, pattern choice, or smell-only review; use php-engineering, php-design-patterns, or php-antipatterns instead.
---

# PHP Testing Quality

## Use When

Use for PHP test design, runner selection, quality commands, and compatibility verification. Use [`php-engineering`](../php-engineering/SKILL.md) for PHP implementation mechanics.

## Workflow

1. Inspect Composer scripts, configured PHPUnit/Pest/Behat, PHPStan/Psalm, PHP_CodeSniffer/PHP-CS-Fixer, Infection, framework harnesses, services, CI, and existing tests before choosing a command.
2. Select the lowest level that proves the changed observable contract, then add integration or browser coverage where the boundary makes unit proof insufficient.
3. Use repository-native commands and report checks actually run.

## Runner And Tool Discovery

Treat `composer.json`, lockfiles, XML/YAML/PHP tool config, bootstrap files, test directories, framework fixtures, Docker/services, and CI as evidence. Do not assume PHPUnit, Pest, Behat, analyzers, formatters, or mutation tools are installed because a PHP project could use them.

## Test Level Selection

- Unit: pure policy, values, errors, state transitions, and edge cases.
- Integration: database, filesystem, HTTP, framework, event, serialization, or container boundaries.
- Contract: public APIs, CLI output, templates, queues, and adapter behavior.
- Behavior/BDD: user-visible workflows and acceptance rules.
- Browser E2E: rendered workflows, JavaScript enhancement, accessibility names, and navigation.
- Property/generative: broad invariants where generated inputs add coverage.
- Mutation: confidence in meaningful test assertions when Infection is configured.
- Static analysis: type and API consistency; it never proves runtime behavior.
- Migration/compatibility: declared supported PHP versions and version-specific paths.

## PHPUnit, Pest, And Behavior Tools

Use the configured PHPUnit or Pest conventions. For BDD discovery load [`behavior-driven-development`](../behavior-driven-development/SKILL.md); for formal `.feature` syntax load [`gherkin`](../gherkin/SKILL.md); for Red-Green-Refactor load [`test-driven-development`](../test-driven-development/SKILL.md); for risk-level strategy review load [`testing-strategy`](../testing-strategy/SKILL.md).

## Integration And Browser Boundaries

Use real supported services and isolated fixtures for persistence, templates, events, and framework behavior. Use [`playwright-e2e`](../playwright-e2e/SKILL.md) for checked-in browser tests; test browser-visible behavior rather than implementation details.

## Fixtures, Doubles, And Determinism

Use explicit clocks and random seeds, isolated databases/filesystems, cleanup owned by each test, and no shared process globals. Double external boundaries by behavior, not private calls. Keep fixtures minimal and readable.

## Compatibility And Migration Tests

When support metadata promises multiple PHP versions, run compatible syntax and behavior lanes for each claimed range. Add focused PHP 8.4 migration tests only for an observable compatibility contract; do not treat an upgrade as proven by parsing alone.

## Command Strategy

Prefer the narrow configured command that covers the changed contract, then the repository's required quality lane. `php -l` is syntax validation only, never behavioral proof. Run formatters and static analyzers when configured; do not invent universal commands. Adaptable examples only: start with a targeted `composer test -- tests/Feature/ChangedTest.php` or configured PHPUnit filter, then run the repository's full Composer/PHPUnit lane when required; do not assume either command exists.

## Review Checklist

- Does each test defend a behavior, boundary, invariant, transition, precedence, or real error?
- Is the selected runner/config actually installed and repository-owned?
- Are deterministic inputs, cleanup, and external service ownership explicit?
- Is compatibility evidence proportional to declared support?

## Anti-Patterns

Avoid tests that assert private plumbing, shared global state, random timing, ambient services, broad mocks, and lint/static-analysis success claimed as product verification.

## Successful Use

Report discovered tools, test level chosen, commands run, covered behavior, and unavailable service or compatibility evidence.
