---
name: test-factories
description: Consolidate test data creation into factories/builders with sensible defaults plus per-test overrides — killing copy-pasted object literals and shared mutable fixtures that couple tests to each other. Use when the same literal is built inline across three or more tests, when a mutated shared fixture makes suite order matter, or when a new required field forces edits across many test files. Restructures setup only; it never changes what a test asserts.
kind: skill
pack: testing
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# test-factories

Test data should be built, not copy-pasted. A test needs a `User` — it asks a factory for one, overriding only the field under test. When every test hand-writes the same 12-field object literal, one schema change breaks forty tests; when they all mutate one shared fixture, they pass in order and fail in isolation. Inline duplicated setup and a shared mutable fixture are the two anti-patterns this skill removes.

## Premise

Find real data-construction rot, no hand-waves. Every finding cites `<path:line>` for the duplicated literal or the shared fixture, names the anti-class (inline-duplication / shared-mutable / no-override / collision), and states the fix as a concrete factory/builder API — `userFactory({ role: 'admin' })`, not "add a factory". A factory that hardcodes every field with no override path is not a fix — it's the shared fixture in a trench coat. "These tests look repetitive" is not a finding; "`order.spec.ts:20-32` rebuilds the same Order literal in 6 tests, differing only in `status`" is.

## Halt conditions

- Halt on a finding without `<path:line>` for the duplicated literal or fixture, plus the count of duplicating tests.
- Halt on proposing a factory with no per-test override path — defaults-only is not a factory.
- Halt on a shared-mutable-fixture claim without demonstrating order dependence (test passes in suite order, fails when run alone / reordered).
- Halt on adding a factory for a field that must be unique (email, slug, external id) without a sequence — a constant default guarantees collisions.

## When to run

- The same object literal is constructed inline across ≥ 3 tests, differing in one or two fields.
- A `beforeEach`/`setup`/module-level fixture is mutated by tests, and suite order matters.
- Adding a required field to a model forces edits across many test files.
- New tests copy an existing test's setup block wholesale.
- Integration tests need related records (an `Order` with a `Customer` and `LineItems`) and rebuild the whole graph by hand each time.

## Adapt to the codebase

Use the stack's idiomatic factory library. Prefer the one already pinned; hand-rolled builders are correct and idiomatic in some ecosystems (Go).

| Stack | Library | Notes |
|---|---|---|
| Ruby | FactoryBot | `factory`/`trait`/`association`; `sequence` for unique fields; `build` vs `create` |
| JS / TS | Fishery + @faker-js | Fishery `Factory.define` with `sequence`; faker for realistic values; test-data-bot as an alt |
| Python | factory_boy + Faker | `SubFactory` for associations; `Sequence`/`Faker` providers; `build` vs `create` strategy |
| Java / Kotlin | Instancio, Java Faker | Instancio auto-populates + `.set(field, val)` overrides; Faker for values |
| PHP | Laravel factories | `definition()` defaults + `state()` overrides + `for()`/`has()` relations; `Sequence` |
| Go | hand-rolled builders | `NewUserBuilder().WithRole("admin").Build()`; functional options; a package counter for sequences |
| C# / .NET | Bogus, AutoFixture | Bogus `Faker<T>` rules; AutoFixture `Customize` + `Build<T>().With(...)` |

If no library is pinned and the ecosystem has a standard one, propose it and STATE the choice — don't silently add a dependency where hand-rolled builders are the local idiom.

## Procedure

1. **Inventory duplication.** Scan tests for repeated object-literal construction of the same type. Group by type; count the duplicating call sites; note which fields actually vary between them.
2. **Find shared mutable fixtures.** Locate module-level / `beforeAll` objects that tests write to. Confirm order dependence: run the suspect test in isolation and reordered — if it flips, it's polluted state, not a passing test.
3. **Design the factory.** Sensible defaults for *every* field (a valid, boring instance), plus an override map/param so a test sets only the field under test. The rule: **only the field being tested should differ from the default.** Everything else is noise the reader must ignore.
4. **Add sequences for unique fields.** Email, username, slug, external id → a monotonic sequence (`user-${n}`, `n@example.test`) so N built instances never collide.
5. **Build associations.** For related graphs, a factory builds its dependencies (`orderFactory` builds a `customer` and `lineItems` unless overridden). Allow passing an existing parent to avoid over-creating.
6. **Separate seed/reference data from per-test data.** Fixed reference rows (currencies, roles, feature flags) belong in a seed loaded once and treated as read-only; anything a test mutates or asserts identity on is built fresh per test.
7. **Keep factories in sync with the schema.** A factory that drifts from the model produces invalid objects that pass unit tests and explode at the DB boundary. Tie the default set to the current schema; a new required column means a new factory default.
8. **Migrate consumers.** Replace inline literals with factory calls; delete the shared mutable fixture; confirm tests still pass *in isolation and reordered*.

## Output

```
Test-data findings — feature/checkout-tests  (base=origin/main)

Test files scanned: 22  |  Inline-literal dup groups: 3  |  Shared mutable fixtures: 1

INLINE DUPLICATION:
  test/order.spec.ts:20-32  (+5 more sites)
    Same 11-field Order literal rebuilt in 6 tests; only `status` varies.
    Fix: orderFactory.build({ status }) — Fishery; defaults cover the other 10 fields.

SHARED MUTABLE FIXTURE (order-dependent):
  test/support/fixtures.ts:8  sharedUser
    Mutated in user_profile.spec.ts:44 (sets role='admin'); leaks into
    permissions.spec.ts which passes only when run after it.
    Proof: `vitest permissions.spec.ts` alone → FAIL.
    Fix: userFactory per test; delete sharedUser.

MISSING SEQUENCE (collision risk):
  test/factories/user.ts:12  email: 'test@example.com'  (constant)
    Building 2 users → unique-index violation.
    Fix: sequence(n => `user-${n}@example.test`).

NO OVERRIDE PATH:
  test/factories/product.ts:5  every test gets identical Product
    Add ({ ...overrides }) merge so price/name can vary per test.
```

## False positives / gotchas

- **Read-only shared fixture is fine.** A shared object that no test mutates isn't the anti-pattern — don't flag it. The defect is *mutation* + order dependence, not sharing per se.
- **Over-building associations.** A factory that eagerly creates a deep graph slows the suite and creates rows tests don't need. Build parents lazily / allow injecting an existing one.
- **`build` vs `create`.** Persisting (`create`) when the test only needs an in-memory object (`build`) is needless DB traffic. Match the strategy to what the test asserts.
- **Faker without a seed.** Random realistic values make failures non-reproducible — seed the faker in test setup, or pin the fields a test asserts on.
- **Factory drift.** A factory whose defaults predate a schema change yields objects that pass unit tests and fail at the persistence boundary. Treat the factory as part of the schema contract.
- **Trait explosion.** Twenty single-use traits are worse than an override param. Reserve named traits/states for genuinely reused variants; use overrides for one-offs.

## Boundary

- `test-doubles.md` owns **behavior** — mocks, stubs, fakes, spies: what a *collaborator* does when the SUT calls it.
- `test-factories` (this) owns **data** — how the *input objects and fixtures* the test operates on are constructed.

A test typically needs both: a factory to build the `User` and `Order` it acts on, and a fake repository (test-doubles) to stand in for the database. Building data through a mock, or scripting behavior through a factory, is using the wrong tool.

Related: `test-doubles`, `@test-engineer`, `test-strategy`.
