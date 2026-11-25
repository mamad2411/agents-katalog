---
name: review-quality
description: Code quality review — correctness hazards, silent failures, structure, tests, and maintainability checklist for reviewing Codex output.
---

# Quality Review (second pass, after conformance)

## Correctness hazards (highest value per minute)

- **Silent failures**: swallowed exceptions, empty catch blocks, errors logged-then-ignored, fallback values masking real failures. Trace every error path to a visible outcome.
- **Edge cases**: empty/null input, zero/one/many, boundary values, unicode, concurrent access. Does the code (and its tests) handle the edges the interview identified?
- **Async/concurrency**: unawaited promises, race conditions on shared state, missing cancellation/cleanup, resource leaks (handles, listeners, timers).
- **State mutation**: in-place mutation of parameters, props, or shared structures.

## Test quality (not just presence)

- Tests assert behavior, not implementation; failure paths tested, not only happy paths.
- Would the tests catch a realistic regression? A test that can't fail is a finding.
- Coverage of NEW code specifically — global % can hide an untested new module.

## Structure & maintainability

- Function > 50 lines, file > 800, nesting > 4 → split (early returns).
- Duplication of logic that exists elsewhere in the repo (Codex can't see the whole repo — you can).
- Dead code, debug prints, commented-out blocks, unused imports left behind.
- Naming that lies (function does more/less than its name says).
- Comments that narrate instead of explaining constraints.

## Calibration

Report findings that change behavior, risk, or maintenance cost. Style nitpicks the project's linter doesn't enforce are LOW at most — don't spend review rounds on them.
