---
name: superforge-test
description: >
  Decide what earns a test, then drive implementation through Red-Green-Refactor
  TDD across Web (Jest, Vitest, Playwright), iOS (Swift Testing, XCTest), and
  Android (JUnit, Compose Test), verifying each red and green state by actually
  running the suite. Covers test granularity (unit / integration / E2E), where
  the mocking boundary belongs, how to recognise a brittle test before it trains
  everyone to ignore failures, why coverage percentage is the wrong target, and
  how to add tests to code that has none. Use when the user says "write tests",
  "TDD", "test first", "add test coverage", "what should I test", "refactor
  safely", "flaky test", "テストを書いて", "テスト先に", "TDD", "何をテストすべき",
  "リファクタリング", "テストが無い", "テストが不安定", or runs /superforge-test.
license: MIT
metadata:
  author: Takao Umehara
  version: "3.0"
compatibility: >
  Standalone.
  Requires a working test runner in the project.
  Updates the proof lines in docs/plan.md when that file exists.
---

# Superforge Test — Multi-Platform Test-Driven Development Engine

Use this skill when implementing new features or refactoring existing code across Web, iOS, and Android. Code written without tests or written *before* tests violates this workflow.

---

## 0. Decide what to test before writing any of it

The cycle below tells you how to write a test. It does not tell you **what to
point it at**, and that is the decision that makes a suite an asset or a tax.
Both failure modes are common: testing everything produces a suite so slow and
brittle that people stop running it; testing nothing produces a codebase nobody
dares change.

The criterion is one line: **a test earns its keep when it would catch a failure
a human would not notice immediately.** Business rules, money, dates, timezones,
units, boundary conditions, and every bug already fixed — yes. Framework
behaviour, pass-throughs, private internals, exact pixels — no.

The full decision table, the granularity rule (**never write at E2E what a unit
test can prove**), the mocking boundary, the brittle-test symptom index, why
coverage percentage is the wrong target, and the order for retrofitting tests to
untested code → **`references/what-to-test.md`**.

---

## The Red-Green-Refactor Cycle

1. **RED**: Write a focused failing test targeting the exact contract.
2. **VERIFY RED**: Run the test runner immediately and confirm clean failure for the *expected reason*.
3. **GREEN**: Write the minimal production code to satisfy the test.
4. **VERIFY GREEN**: Re-run the test and confirm clean passing output.
5. **REFACTOR**: Polish code for readability, dynamic layout, and performance without breaking tests.

---

## Test Runners by Platform

- **Web (JS/TS)**: `npm test -- path/to/spec.test.ts` (Jest / Vitest / Playwright).
- **iOS Native**: `xcodebuild test -scheme <Scheme> -destination 'platform=iOS Simulator,name=iPhone 16'` or `swift test`.
- **Android Native**: `./gradlew test` (Unit tests) or `./gradlew connectedCheck` (Espresso/Compose UI tests).

---

## Deeper reference

**`references/what-to-test.md`** — what earns a test and what does not, the
unit / integration / E2E cost ladder, mock at the boundary of what you control
and never inside it, the six brittle-test symptoms and their causes, coverage
as a map of what ran rather than of what was checked, and the four-step order
for adding tests to a codebase that has none (at the bug, at the change, at the
seam, at the boundary).

---

## Artifact

Tests are the artifact. When `docs/plan.md` exists, fill in the proof line of
each task with the exact command that proves it, so an unattended run can
verify itself without a human interpreting the output.

A test that locks a fixed bug is also what `superforge-debug` records as
`Locked by:` in `docs/failforward.md` — when that line says 無し, this skill is
the one that should have run. **A security fix earns a test unconditionally**
(`superforge-secure`): an authorization check that regresses silently is the
worst case in §1's first row.

## Delegate when a sharper skill is installed

`test-driven-development`, `tdd-feature`, `tdd-bug-fix` (discipline) ·
`tdd-refactor-guard`, `characterization-test-generator` (refactor safety) ·
`test-generator`, `test-data-factory`, `integration-test-scaffold`,
`snapshot-test-setup` (scaffolding) · `test-contract`, `test-spec`.
