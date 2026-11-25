---
name: phpunit-testing
description: Write and run PHPUnit tests. Use whenever a new function/class/endpoint is added or changed, to add or update its unit/integration tests, run the suite (or a single test), and keep coverage meaningful. Default to test-alongside-every-change.
---

# PHPUnit Testing

Policy: **every new or changed function gets a test in the same change.** Don't consider a feature done until its tests exist and pass.

## Layout & setup
- Tests in `tests/`, mirroring `src/` namespaces (PSR-4 `Tests\` autoload in `composer.json` `autoload-dev`).
- Config in `phpunit.xml`. Use the current PHPUnit major (11/12): attributes (`#[Test]`, `#[DataProvider]`, `#[CoversClass]`) over the old `@` annotations.
- Name files `*Test.php`, classes `final class XxxTest extends TestCase`.

## Running
```bash
composer install
vendor/bin/phpunit                          # full suite
vendor/bin/phpunit tests/Unit/FooTest.php   # one file
vendor/bin/phpunit --filter testCreatesUser # one test by name
vendor/bin/phpunit --coverage-text          # coverage (needs Xdebug/PCOV)
```
If no Composer/PHPUnit setup exists yet, scaffold it: `composer require --dev phpunit/phpunit`, add a `phpunit.xml`, wire `autoload-dev`, and add a `composer test` script.

## Writing good tests
- **Arrange-Act-Assert**, one behavior per test, descriptive names (`testRejectsDuplicateEmail`).
- Cover happy path, edge cases, and failure/exception paths (`expectException`). Use `#[DataProvider]` for input matrices.
- Isolate units: mock collaborators (DB, Redis, HTTP) with test doubles; keep true integration tests separate (`tests/Integration/`) with real MySQL/Redis fixtures and transactional rollback.
- Deterministic and fast — no sleeps, no network in unit tests, no shared mutable state between tests.
- Test behavior and contracts, not private implementation details.

## Always
After adding code, add/adjust the test, run the relevant test, and report pass/fail with the actual output. For broad test-strategy or non-PHPUnit automation, use `automation-tester-specialist`.
