---
name: test-strategy
description: Decides what to test and at which level, then writes fast, deterministic tests that check behavior rather than implementation details. Use when planning how a feature or system should be tested, choosing between unit, integration, contract and end-to-end tests, deciding what to mock, fixing flaky tests, or adding a regression test for a bug fix. For writing unit tests for a specific change, use unit-testing.
license: MIT
---

# Test Strategy

A good test fails when the behavior breaks, and only then. Test what the code promises to its callers, at the cheapest level that can catch the bug you care about, and make every test deterministic.

## Workflow

1. **Learn the project's conventions.** Find the test framework, folder layout, naming style, fixtures and factories, and how CI runs the tests. Match them. Run the existing suite once to get a baseline (pass/fail, runtime, known flaky tests).
2. **List the behaviors.** For the code under test, write down inputs and the outputs or side effects they should produce, including error cases and edge cases (empty, null, zero, boundaries, duplicates, invalid input, permissions). This list is your test list.
3. **Choose a level for each behavior** (table below).
4. **Decide on test doubles** (rules below).
5. **Write the tests** one behavior at a time, using Arrange-Act-Assert.
6. **Prove each test can fail.** Temporarily break the code (or invert the expectation), watch the test fail with a clear message, then revert. A test you have never seen fail may test nothing.
7. **Run the whole suite,** then run the new tests several times and in random order if the framework supports it. Check runtime.

Per-framework commands (single test, filter, rerun failures, random order, repeat, coverage) are in [references/framework-commands.md](references/framework-commands.md).

## Choosing the level

| Level | Use for | Strength | Cost |
|---|---|---|---|
| **Unit** (no I/O) | Business rules, calculations, parsing, validation, state machines, branching logic | Milliseconds; failures point at the exact problem | Misses wiring and integration bugs; brittle if tied to internals |
| **Integration** (real database, file system, HTTP inside the service, framework wiring) | Queries and ORM mappings, transactions, serialization, migrations, dependency injection, middleware | Catches real mismatches between your code and its infrastructure | Slower; needs setup and isolation |
| **Contract** (consumer-driven contracts or schema checks) | APIs and events between services or teams | Catches breaking changes without deploying everything | Needs discipline on both sides |
| **End-to-end** (UI or full deployed system) | A few critical user journeys: sign-up, login, checkout | Highest confidence that the system works | Slowest and most flaky; keep the number small |

Rules of thumb:

- Put most logic tests at the unit level, with I/O pushed to the edges of the code.
- Test every query or repository against the **same database engine** you run in production (for example with Testcontainers or a disposable local instance). An in-memory substitute such as SQLite standing in for PostgreSQL hides real bugs.
- Keep end-to-end tests for journeys whose failure would be an incident.
- The shape of the suite ("pyramid" or "trophy") matters less than fast feedback and real confidence.

## Test doubles

- **Replace what is slow, non-deterministic or outside your control:** third-party HTTP APIs, payment providers, email and SMS, the clock, randomness. Use a fake server where possible (WireMock, MSW, `responses`/`respx`, Go's `httptest.Server`).
- **Do not mock what you do not own directly.** Wrap the third-party client in your own small adapter and fake the adapter; test the adapter itself against a fake server or a sandbox.
- **Prefer fakes over mocks.** An in-memory implementation of a repository or queue gives more realistic behavior than a mock with scripted call expectations.
- **Assert outcomes, not calls.** Check the returned value or the resulting state. Verify interactions only when the interaction *is* the behavior ("sends exactly one email", "does not charge twice").
- **Never mock the unit under test, value objects, or simple data structures.**
- If a test needs many mocks, the code probably has too many dependencies; say so rather than piling on mocks.

## Determinism

| Source of flakiness | Fix |
|---|---|
| Current time | Inject a clock or freeze time: `freezegun` or `time-machine` (Python), `vi.useFakeTimers()` / `jest.useFakeTimers()`, `Clock.fixed(...)` (Java), `TimeProvider` with `FakeTimeProvider` (.NET 8+), a `now func() time.Time` parameter (Go) |
| Randomness | Seed the generator or inject it; log the seed on failure |
| Network | No real external calls in unit or integration tests; use fake servers |
| Ordering | Never depend on test execution order, hash map iteration order, or database row order without `ORDER BY` |
| Async and concurrency | Wait for a condition or await completion; never `sleep` a fixed time |
| Shared state | Each test creates its own data (unique IDs, transaction rollback, fresh schema); reset globals, singletons and environment variables |
| Environment | Pin timezone and locale in test config (for example `TZ=UTC`), use path APIs instead of string paths, avoid machine-specific ports (bind to port 0) |

Detailed diagnosis and fixes are in [references/flaky-tests.md](references/flaky-tests.md).

## Writing tests

- **Name the behavior:** `refund_fails_when_order_already_refunded`, `it("rejects expired tokens")`. The name should explain the failure without reading the body.
- **Arrange-Act-Assert,** separated by blank lines. One behavior per test; several assertions are fine if they describe the same outcome.
- **Show only what matters:** build data with factories or builders that have sensible defaults, and set only the fields this test depends on.
- **No logic in tests** (loops, conditionals). Use parameterized tests instead: `@pytest.mark.parametrize`, `it.each` / `test.each`, Go table-driven tests with `t.Run`, JUnit `@ParameterizedTest`, xUnit `[Theory]` with `[InlineData]`, NUnit `[TestCase]`.
- **Assert precisely:** specific values, specific error types and messages, not just "did not throw" or "is truthy".
- **Snapshot tests** only for stable, human-reviewed output. Review snapshot diffs; never update them blindly to make a test pass.

## Property-based and fuzz testing

When the input space is large (parsers, serializers, encoders, math, sorting, state machines), assert **properties** that hold for all inputs instead of a handful of examples:

- Round trip: `decode(encode(x)) == x`.
- Invariants: output is sorted, totals balance, length is preserved.
- Idempotence: `f(f(x)) == f(x)`.
- Never crashes on any input.

Tools: Hypothesis (Python), fast-check (JS/TS), jqwik (Java), FsCheck (.NET), proptest (Rust), Go's built-in fuzzing (`go test -fuzz=FuzzParse`). Keep any failing example the tool finds as a regular regression test.

## Bug fixes: failing test first

1. Write a test that reproduces the bug at the lowest level that shows it.
2. Run it and confirm it fails for the expected reason.
3. Fix the code; the test passes.
4. Name the test after the behavior, not the ticket number (reference the ticket in a comment if useful).

## Coverage

Use coverage to find **untested branches in the code you changed**, especially error handling. Do not chase a percentage: 100% line coverage with weak assertions proves little. To check whether tests actually detect bugs in critical modules, use mutation testing (Stryker for JS/TS and .NET, PIT for Java, mutmut for Python, cargo-mutants for Rust).

## Anti-patterns

- **Testing implementation:** asserting private methods, internal call order or exact SQL strings, so every refactor breaks tests that should pass.
- **Over-mocking:** the test passes while the real integration is broken.
- **Fixed sleeps** to wait for async work.
- **Tautological tests:** asserting that a mock returns what you told it to return.
- **Shared mutable fixtures** that make tests depend on each other.
- **Deleting or skipping failing tests** to get green. Quarantine with an owner and a ticket instead, and fix the cause.
- **A large end-to-end suite as the main safety net:** slow, flaky, and failures are hard to localize.
- **Testing the framework or library** instead of your code.
- **Changing the test and the code together** without ever seeing the test fail.

## Done when

- Every behavior on the test list has a test at an appropriate level, including error paths.
- Each new test has been seen failing for the right reason.
- New tests pass repeatedly and in random order; no real network or wall-clock dependence.
- The full suite passes and its runtime is still acceptable.

## References

- [references/framework-commands.md](references/framework-commands.md) — read for exact commands in pytest, Jest, Vitest, go test, JUnit 5 (Maven/Gradle), dotnet test and cargo.
- [references/flaky-tests.md](references/flaky-tests.md) — read when a test passes and fails without code changes, or fails only in CI.
