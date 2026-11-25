---
name: grimoire-test
description: Write unit tests that verify module behavior through isolated, well-structured test cases.
---

# Purpose

Write unit tests that verify module behavior — not implementation — through isolated, predictable test cases.

# Scope

This skill controls how unit tests are designed, structured, and written.

Outside scope: integration tests, E2E tests, performance tests, test framework selection, CI configuration.

# Leading words

- **SUT** — System Under Test, the module being tested
- **AAA** — Arrange → Act → Assert, the required test structure
- **test double** — Mock, Fake, or Stub that replaces an external dependency
- **behavior test** — a test that verifies public API outcome, not internal state
- **isolation** — replacing every external dependency with a test double

# Workflow

## 1. Analyze the target

Identify:
- SUT: what module, class, or function is under test?
- Public API: what behaviors does it expose to callers?
- Dependencies: what external resources does it consume (database, network, filesystem, other modules)?

Output: a brief description covering SUT boundary, public API surface, and dependency list.

---

## 2. Check testability

Before designing test cases, evaluate whether the SUT can be tested cleanly.

**Stop and suggest refactoring when:**
- The SUT has more than 3 dependencies → suggest splitting responsibilities
- A dependency cannot be replaced by a test double (e.g., hard-coded instantiation) → suggest dependency injection
- The SUT mixes business logic with I/O (e.g., HTTP calls inside domain logic) → suggest separating concerns
- Testing a behavior requires mocking the SUT itself → suggest extracting the behavior into a separate module
- Setup would require more than ~5 lines of mock configuration → suggest reducing coupling

**How to suggest:**
- Point to the specific code location causing the problem
- Describe why it makes testing hard (which principle it violates)
- Give one concrete refactoring direction, not a full rewrite
- Ask the user whether to proceed with refactoring or force the test anyway

Output: either a clean testability assessment (proceed to step 3) or a list of refactoring suggestions with the question: "Refactor first, or force the test?"

---

## 3. Design test cases

For each public behavior, list:
- **Normal path** — the expected happy-path input and output
- **Edge cases** — boundary values, empty/null/undefined, maximum/minimum ranges
- **Error cases** — how the SUT reports failures to the caller
- **State transitions** — if the SUT is stateful, how it moves between states

Output: a test case list. Every public behavior has at least one normal-path case plus edge and error cases where applicable.

---

## 4. Plan isolation

For each dependency identified in step 1:
- **Mock** — use when the test must verify that a specific call was made (behavior verification)
- **Stub** — use when the test only needs a controlled return value (state verification)
- **Fake** — use when a lightweight in-memory replacement is simpler than mocking

Output: every dependency has an assigned isolation strategy.

---

## 5. Write tests

Write each test case following these rules:

**Structure: AAA**
```
// Arrange — build SUT, configure test doubles, prepare input
// Act — call one public behavior
// Assert — verify the observable outcome
```

**Naming**: `should_[expected behavior]_when_[condition]`

**Rules**:
- Assert on public API return values, thrown errors, or calls to test doubles — never on internal fields
- Exactly one behavior per test
- No shared mutable state between tests

Output: a test file where every planned case has a corresponding AAA test method.

---

## 6. Run tests

Execute the test suite and verify every test passes.

**Rules:**
- Run all tests in the test file, not just the newly written ones
- If a test fails, diagnose and fix before proceeding — do not leave failing tests behind
- If the failure is in the test (not the SUT), fix the test
- If the failure is in the SUT, report it: the test caught a bug

Output: full test run with all tests passing. No skipped or pending tests.

---

## 7. Verify

Run the checklist:
- [ ] Test verifies behavior, not internal state
- [ ] Test is independent (no shared mutable fixture, no ordering dependency)
- [ ] Every external dependency is replaced by a test double
- [ ] Normal, edge, error, and state cases are covered
- [ ] AAA structure is followed, test name expresses behavior
- [ ] No test exists solely for coverage

Output: all items pass. If any item fails, fix the test — not the checklist.

---

# References

- [principles.md](./references/principles.md) — the six testing principles explained
- [patterns.md](./references/patterns.md) — AAA, naming conventions, test double decision guide
- [examples.md](./references/examples.md) — side-by-side good vs bad test examples
