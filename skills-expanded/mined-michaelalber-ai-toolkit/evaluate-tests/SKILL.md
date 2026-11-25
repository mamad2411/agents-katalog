---
name: evaluate-tests
audience: team
description: >
  Audits existing tests in two modes: (1) test-file quality — grades tests against Beck's
  behavioral and structure-insensitive criteria, flagging implementation-coupled, fragile, and
  theater tests with a prioritized rewrite list; (2) TDD compliance — analyzes git history for
  test-first discipline, producing a 0-25 scorecard with AI anti-pattern findings. Use when
  auditing inherited suites, checking AI-generated tests before merge, prepping for safe
  refactoring, or verifying TDD was followed. Not for writing new tests (tdd-loop), or when there are
  no tests yet.
---

# Evaluate Tests

> "If tests break when you rename a private method, your tests are describing the solution,
> not the problem."
> — Adapted from Kent Beck

## Core Philosophy

A behavioral test fails when the observable outcome breaks; an implementation-coupled test fails
when internals change even if behavior is identical. Only the first kind makes refactoring safe.
Tests written after implementation test different things than tests written first — so this skill
audits both the tests themselves and the discipline that produced them.

| Mode | Input | Output | Use when |
|------|-------|--------|----------|
| **1 · Test-file quality** | a test file or directory | per-test classification + prioritized rewrite list | auditing whether existing tests are behavioral and refactor-safe |
| **2 · TDD compliance** | git commit history (+ test/impl files) | 0–25 compliance scorecard + anti-pattern findings | verifying test-first discipline was actually followed |

Pick the mode from the request. Run both for a full audit — Mode 1's findings feed the Behavioral
and Coverage categories of Mode 2's scorecard.

**Non-Negotiable Constraints:**
1. **Evidence-based only** — never claim compliance without commit-history proof; never classify a test without reading it.
2. **Every test gets exactly one class** — PASS, COUPLED, FRAGILE, or THEATER — with a reason and a suggested fix.
3. **Bounded scope** — on a directory, evaluate the most-changed test files first; ask before evaluating more than 20 tests in one turn.
4. **Constructive, in context** — findings drive improvement, not punishment; account for legacy code, time pressure, and learning curves before scoring.

## Workflow

### Mode 1 — Test-File Quality

1. **Behavioral?** Does the assertion target a return value, publicly visible state, or a side effect via a public interface (behavioral) — or mock call counts, private fields, internal call order (coupled)? A behavioral failure message points to the *what* ("Expected 42, got 0"); a coupled one to the *how* ("Expected save() to be called once").
2. **Structure-insensitive?** If every private method and field were renamed, would this test break? If yes, it is structure-coupled.
3. **Horizontal slicing?** A commit with 3+ test stubs followed by one with all implementations, or tests asserting on code that clearly pre-existed them.
4. **Classify** each test:

| Class | Definition | Action |
|-------|-----------|--------|
| **PASS** | Behavioral + structure-insensitive | Keep |
| **COUPLED** | Asserts on implementation detail (call counts, private state, internal call order) | Rewrite: assert on observable outcome instead |
| **FRAGILE** | Survives behavior changes but breaks on structural refactors | Rewrite: remove internal references |
| **THEATER** | Passes trivially; no assertion or assertion always passes | Strengthen or delete |

Concrete rewrite examples by language: `references/coupling-patterns.md`.

### Mode 2 — TDD Compliance (commit-history audit)

1. **Gather evidence** — chronological `git log`, test + implementation file contents, coverage report (if available), test-run results.
2. **Analyze commit order** — did a failing-test commit precede each implementation commit? Flag commits containing both test and impl, and impl commits with no preceding test.
3. **Analyze test quality** — run Mode 1's classification on the changed tests.
4. **Check coverage quality** — real coverage (fails when behavior breaks; edge and error paths covered) vs theater (passes with broken behavior; no assertions; happy path only).
5. **Detect AI anti-patterns:**

| Anti-Pattern | Detection Signal |
|---|---|
| **Test-After Implementation** | Both test and impl in one commit; no failing-test commit before the impl commit |
| **Over-Mocking** | `assert_called_with(...)` on implementation-internal methods |
| **Happy Path Only** | Test inventory missing zero / overflow / invalid-input cases |
| **Assert-Free Tests** | Zero assertion statements in the test body |
| **Implementation Coupling** | `_private_method` / `_internal_state` references in test assertions |
| **Copy-Paste Tests** | Test names like `test_X_1`, `test_X_2` with only value differences |

6. **Score** the five categories 0–5 each (`references/compliance-scoring.md`).

**Exit criteria:** Mode 1 — every in-scope test classified with reason and fix; Mode 2 — every commit in the period classified and all five categories scored with cited commit evidence.

## State Block

```xml
<evaluate-tests-state>
  mode: 1-quality | 2-compliance | both
  scope: [file, directory, or repo/branch + date range]
  tests_evaluated: [count]
  classes: PASS=[n] COUPLED=[n] FRAGILE=[n] THEATER=[n]
  commits_analyzed: [count | n/a]
  compliance_score: [X/25 | n/a]
  anti_patterns: [list | none]
  last_action: [what was just done]
  next_action: [what should happen next]
</evaluate-tests-state>
```

## Output Template

- Mode 1 Test Evaluation report (summary, prioritized rewrite list, horizontal-slice signals) and the Mode 2 TDD Compliance Scorecard (+ commit-order table): `references/output-templates.md`
- Scoring methodology for the scorecard: `references/compliance-scoring.md`
- AI-specific anti-pattern catalog with examples: `references/ai-antipatterns.md`

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `tdd-loop` | Writes new tests test-first; this skill audits tests that already exist. Mode 2 verifies its discipline was followed. |
| `test-scaffold` | .NET test conventions; COUPLED/FRAGILE rewrites in C# should follow its naming and mocking patterns. |
| `automated-code-review` | Its maintainability category covers test code in a diff; use this skill for a dedicated suite audit. |
| `technical-debt-assessor` | A high COUPLED/FRAGILE count is test debt — quantify its cost-to-carry there. |
