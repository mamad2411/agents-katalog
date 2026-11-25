---
name: recording-studio-tests
description: Add or review Minitest coverage for Recording Studio gems and dummy apps. Use when writing tests, checking coverage, or validating engine and host-app wiring before merge.
---

# Recording Studio tests

## When to use

- Adding or updating Minitest coverage
- Writing regression tests for generators, hooks, services, or engine wiring
- Verifying dummy-app boot, assets, or migrations
- Reviewing whether validation coverage is enough before merge

## Suites

Recording Studio gems have two suites. Cover both, and run both before considering work complete:

- Gem suite under `test/` for engine and library behavior
- Dummy app suite under `test/dummy/test/` for host-app wiring and integration

Do not treat the gem suite alone as enough. Dummy-app tests catch mount, initializer, route, and asset wiring that unit tests miss.

## Coverage target

Aim for high coverage. The usual working target is about **94%**, but that number is a team convention, not a hard law. Use it as the default bar:

- If coverage is below ~94%, add tests until the suite is back near that level.
- Prefer meaningful coverage of changed behavior over chasing the number with low-value assertions.
- Never delete, stub out, or bypass production code to inflate coverage or make tests pass.

## Procedure

1. Identify the narrowest tests that can falsify the change in the gem suite and, when wiring is involved, the dummy app suite.
2. Add focused happy-path, failure-path, and edge-case coverage.
3. Prefer unit tests for POROs and services, and thin integration tests for engine and dummy-app wiring.
4. Preserve public behavior.
5. Run the gem suite from the repository root (typically `bundle exec rake test`).
6. Run the dummy app suite as well (typically tests under `test/dummy/test/`, or the repo's documented dummy test command).
7. If dummy-app boot, assets, or migrations changed, also run the dummy app setup used in CI.

## Recording Studio expectations

- Cover configuration defaults and overrides.
- Cover hook ordering, arguments, and error isolation.
- Assert immutable recordables and event history on write paths.
- Dummy-app tests should cover engine **mount**, initializer/route wiring, and **Accessible** (or the mixin under test) — not only a unit of library code.
- Keep tests fast, deterministic, and scoped to the change.
