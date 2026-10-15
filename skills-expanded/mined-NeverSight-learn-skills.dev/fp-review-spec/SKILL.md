---
name: fp-review-spec
description: Validate that E2E_TESTS.md specification files are complete and well-structured
---

# Review E2E Spec

Validate that `E2E_TESTS.md` specification files are complete, well-structured, and follow the required format. This is a read-only command — it reports findings but does not modify any files.

Additional instructions from the user: "$ARGUMENTS". Ignore if empty.

## Phase 1: Discover

1. Find all `E2E_TESTS.md` files in the project.
2. Read each one fully.

## Phase 2: Validate Structure

For each `E2E_TESTS.md`, check:

### Required elements
- [ ] Has an **Index** section with a markdown link to every suite
- [ ] Has at least one suite (H2 heading)
- [ ] Every suite has a `### Preconditions` section
- [ ] Every suite has a `### Features` section with at least one feature
- [ ] Features are **flat peer headings** directly under `### Features` — no intermediate category headings (e.g., `#### Core`, `#### Edge`, `#### Error`). Categories are specified only via `<!-- category: ... -->` HTML comments.
- [ ] Every suite has a `### Postconditions` section
- [ ] Every feature (H4 heading) has at least one assertion bullet

### Metadata
- [ ] Every feature has a `<!-- category: ... -->` comment
- [ ] Category values are valid: `core`, `edge`, `error`, `side-effect`, `idempotency`
- [ ] Features with `<!-- skip: ... -->` have a documented skip reason

### Quality
- [ ] No duplicate feature names within a suite
- [ ] Preconditions are achievable programmatically (no manual steps)
- [ ] Assertions are concrete and testable (not vague like "works correctly")
- [ ] Present tense, declarative style ("Creates file" not "Should create file")

### Category coverage
For each suite, check that there is reasonable category diversity:
- At minimum, `core` features should exist
- Warn if no `error` features exist (error handling is often overlooked)
- Note if `edge` and `idempotency` are missing (informational, not blocking)

## Phase 3: Report

Present findings per file:

```
Spec Review: packages/cli/E2E_TESTS.md
==========================================

Structure:  PASS (4 suites, 23 features)
Metadata:   WARN (2 features missing category)
Quality:    PASS

Issues:
  WARNING  Feature "Handle edge case" in suite "Task Creation" has no category comment
  WARNING  Feature "Process request" in suite "API" has no category comment
  INFO     Suite "Push" has no error-category features
  INFO     Suite "Init" has no idempotency-category features

Category distribution:
  core:        14 features
  edge:         3 features
  error:        4 features
  side-effect:  2 features
  idempotency:  0 features  ← consider adding

Summary: 2 warnings, 2 info notes
```

Do NOT modify the spec files. Report only.
