---
description: "Use when implementing features, writing tests, or following the TDD/ATDD development cycle. Covers the spec-first workflow, red-green-refactor cycle, and how specs, tests, and implementation relate. Trigger phrases: ATDD, TDD, spec-first, acceptance tests, red-green-refactor, feature implementation, test-driven."
---

# ATDD Workflow

## The Cycle

```
Requirements → Spec → Acceptance Tests → Red → Green → Refactor → Review
```

## Phase Rules

### Spec Phase

- Every feature starts with a spec in `specs/`
- Current truth: `specs/capabilities/<domain>/behavior.feature` + `rules.md`
- Work in flight: `specs/changes/<name>/` — `proposal.md`, `delta.feature`, `delta-rules.md`,
  `tasks.md`. A change never edits a capability directly; the delta merges in at Phase 7
- Specs define **behavior** (what), not implementation (how)
- Spec is the source of truth; code must match the spec, not the reverse

### Test Phase (Red)

- Write test stubs for every Gherkin scenario before writing any production code
- Run tests to confirm they fail **for the right reason**
  - "Wrong-reason" failures (syntax errors, import errors) must be fixed before implementing
  - A test that passes without implementation is invalid — the test itself is broken
- Do not proceed to implementation until all stubs are confirmed red

### Implementation Phase (Green)

- **Before writing any production code**, re-read `docs/project-profile.md` (the `Conventions`
  and `Reference Files` sections) and open at least one reference file from the same layer you
  are about to write. State explicitly which conventions you will follow.
- Implement only what is required to make failing tests pass
- Work scenario by scenario, in priority order: `@smoke` → `@happy-path` → `@edge-case` → `@error`
- **Mirror** the patterns recorded in the project profile — do not introduce a new architecture,
  error-handling style, validation library, or naming scheme without explicit user approval
- Never add logic not demanded by a failing test
- If you find yourself writing "just in case" code — stop and delete it

### Refactor Phase

- Refactor only when **all** tests are green
- Run tests after every change — if tests break, revert the change
- Refactoring changes structure without changing behavior
- Do not add features during refactor

### Review Phase — Spec & Doc Sync (Hard Gate)

This is a **blocking** gate. Repair drift in-phase, do not defer.

- Every scenario must have a corresponding test that would fail if behavior were removed
- Every numbered business rule in the technical spec must be enforced by a test
- Implementations without test coverage must have explicit justification
- The `.feature` file must accurately describe what the code does today — fix drift now
- Classify each repair ADDED / MODIFIED / REMOVED. A REMOVED means a guarantee the spec made is
  no longer promised — it is a spec weakening, needs confirmation, and is never applied under
  "update the spec to match the code"
- `README.md` must be updated if the feature is user-visible
- `docs/project-profile.md` must be updated if Phase 3 introduced a new convention or dependency
- Re-run the full test suite and all quality gates after every fix above

---

## Spec Change Protocol

When requirements change:

1. Update the spec first — `specs/changes/<name>/delta.feature` while in flight, or the
   capability's `behavior.feature` if already archived
2. Update `delta-rules.md` (or the capability's `rules.md`) if needed
3. Update or add tests to match the new spec
4. Confirm new/changed tests are red
5. Update implementation to pass the new tests
6. Confirm all tests green
7. Update `README.md` and any other user-facing docs that describe the changed behavior — this
   is part of the change, not a follow-up
8. Update `docs/project-profile.md` if a new convention or dependency was introduced

**Never** update implementation to accommodate changed behavior without first updating the spec.
**Never** declare a behavior change "done" while the spec, README, or project profile still
describe the old behavior.

---

## Tag Priority Order

When implementing incrementally, work in this order:

| Tag           | Priority     | Description                  |
| ------------- | ------------ | ---------------------------- |
| `@smoke`      | 1st          | Must-pass critical path      |
| `@happy-path` | 2nd          | Primary success scenarios    |
| `@edge-case`  | 3rd          | Boundary and unusual inputs  |
| `@error`      | 4th          | Error handling and sad paths |
| `@wip`        | Skip         | Not yet ready to implement   |
| `@regression` | After errors | Previously found bugs        |
