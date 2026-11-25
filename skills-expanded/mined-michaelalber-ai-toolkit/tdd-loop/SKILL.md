---
name: tdd-loop
audience: team
description: >
  The canonical RED-GREEN-REFACTOR inner loop. Enforces behavioral, structure-insensitive tests
  and prohibits horizontal slicing. Use when writing any new code test-first, managing TDD phase
  transitions, or as the inner loop for qrspi-implement, qraspi-implement, or any other
  implementation skill. Do NOT use to audit existing test suites — use evaluate-tests instead.
---

# TDD (Red-Green-Refactor)

> "Write tests that are sensitive to behavior changes, insensitive to structure changes."
> — Kent Beck

## Two Critical Properties

Every test must satisfy both before leaving RED:

| Property | A compliant test... | A violation looks like |
|----------|---------------------|------------------------|
| **Behavioral** | fails when the observable outcome breaks | `assert repo.save.called` — verifies a method was called, not what the system produced |
| **Structure-insensitive** | survives a rename-only or extract-method refactor | `assert order._total == 100` — reads internal state; breaks on any rename |

## The Failure Mode: Horizontal Slicing

The most common TDD failure in AI-generated code:

```python
# WRONG — horizontal slice
def test_register(): ...
def test_login(): ...
def test_logout(): ...
# ... then all implementation
class Auth: ...
```

```python
# RIGHT — vertical slice
def test_register(): ...    # one test
class Auth:                 # minimal code to pass it
    def register(): ...
# refactor → commit → next test
def test_login(): ...
```

Horizontal slicing produces tests that were never red, implementations that were never minimal,
and refactoring that was never constrained by a safety net. **Never accumulate unimplemented tests.**

## The Cycle — One test → one implementation → repeat

### RED
1. Write ONE failing test for the next smallest observable behavior
2. Run the suite — the new test must fail for a semantic reason (not import/syntax)
3. All other tests must still pass

### GREEN
1. Write the minimum code to pass the failing test — nothing it does not require (no unrequested error handling, config, edge cases, or "while I'm here" features)
2. Prefer: Fake It (hardcode) → Obvious Implementation → Triangulation
3. Run the suite — all tests must pass
4. Strategies & per-language idioms (.NET/Python/PHP/TS): [green idioms](references/green-minimal-patterns.md) on demand, plus per-language `references/green-dotnet-idioms.md`, `references/green-python-idioms.md`, `references/green-php-idioms.md`, `references/green-typescript-idioms.md`; for .NET test structure see `test-scaffold`

### REFACTOR
1. One structural change at a time — behavior must not change (no bug fixes, no new features; those start a new RED)
2. Replacing a fake with real logic is allowed only if no test-free branch comes with it. Handling an input shape no test uses yet is new behavior: write its RED test first, and never claim behavior no test covers
3. Run tests after every change — revert immediately if red
4. Smell→refactoring recipes: [code smells](references/code-smells.md) · [refactoring catalog](references/refactoring-catalog.md) on demand

## Per-Cycle Self-Check

- [ ] This test was red before I wrote any implementation
- [ ] This test asserts an observable outcome, not a method call or internal state
- [ ] A rename-only refactor would NOT break this test
- [ ] My implementation passes this test and no others I have not written yet
- [ ] All tests are green entering REFACTOR

## State Block

```
<tdd-state>
phase: RED | GREEN | REFACTOR
iteration: N
current_test: [test name]
failure_reason: [semantic description — not "syntax error"]
tests_passing: true | false
</tdd-state>
```

Field rules and examples: `references/state-management.md`. Detailed transition gates between phases: `references/phase-transitions.md`.

## Modes & Companions

The one canonical loop (GREEN/REFACTOR depth in `references/` above). Companions are *modes* and *audits*, not alternatives:

| Need | Skill |
|------|-------|
| AI drives all phases autonomously (defers here for mechanics) | `tdd-agent` (agent) |
| Audit test quality or TDD compliance after the fact | `evaluate-tests` |
| .NET test conventions — xUnit / AAA / mocks | `test-scaffold` |
| RED before/after examples | [Behavioral Examples](references/behavioral-examples.md) |
