---
name: php-antipatterns
description: Evidence-backed PHP smell review and refactoring guidance. Use when auditing or refactoring PHP for dynamic properties, magic accessors, weak types, global state, unsafe loading, injection risks, framework leakage, brittle tests, dependency sprawl, or PHP 8.4 migration smells. Do not use for ordinary implementation, pattern selection, or test execution; use php-engineering, php-design-patterns, or php-testing-quality instead.
---

# PHP Anti-Patterns

## Use When

Use for focused PHP review or refactoring with code evidence and a plausible maintenance, correctness, or security consequence. Route implementation to [`php-engineering`](../php-engineering/SKILL.md), positive design choices to [`php-design-patterns`](../php-design-patterns/SKILL.md), and test lanes to [`php-testing-quality`](../php-testing-quality/SKILL.md).

## Generated Material Boundary

Treat generated, vendored, framework-cache, and dependency material as evidence, not refactoring targets. Establish ownership before proposing changes; route dependency provenance and executable Composer inputs to [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md).

## Common Anti-Patterns

Look for dynamic-property bags, magic accessor overuse, associative-array domain models, weak or implicit types, loose comparison and truthiness traps, global/service-locator state, include-time side effects, broad exception swallowing, error suppression, unsafe `eval`/deserialization/file inclusion, and string-built SQL/HTML/JavaScript.

## PHP 8.4 Migration Smells

Flag implicitly nullable declarations, property hooks with I/O or recursive/surprising behavior, assuming asymmetric visibility makes referenced objects transitively immutable, and upgrading to a PHP 8.4 feature without proving the supported runtime. Keep feature facts in [`php-84-migration.md`](../php-engineering/references/php-84-migration.md), not in this review catalog.

## Architecture And Method Smells

Flag framework/ORM leakage into domain policy, generic CRUD repositories, inheritance-heavy abstractions, service bags, wrappers with no invariant or substitution seam, and transaction or resource ownership split across layers.

## Template And Framework Smells

Flag controllers that build HTML, templates that implement policy, raw data crossing into executable JavaScript, and framework globals entering domain logic. Use context-aware encoding and explicit render data instead. Recognize host-required entry guards, including Piwigo direct-entry guards, rather than flagging them generically.

## Test Smells

Flag excessive mocks, nondeterministic fixtures, shared process globals, tests coupled to private plumbing, and static-analysis or syntax-only checks presented as behavioral proof.

## Refactoring Prompts

Ask what invariant, boundary, or observable behavior the code protects. Replace bags with typed values, loose comparisons with explicit intent, globals with injected dependencies, and string construction with structured APIs. Keep changes small and migrate every caller.

## Reporting Rules

Report only evidence-backed findings: location, concrete path to failure or maintenance cost, severity proportionate to impact, and a smallest safe correction. Do not report style preference as a defect. Use [`code-review`](../code-review/SKILL.md) and [`review-verification-protocol`](../review-verification-protocol/SKILL.md) for reported findings.
