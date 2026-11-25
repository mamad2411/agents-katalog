---
name: minimal-diff
last_reviewed: 2026-09-06
group: Build
description: >-
  Make the smallest correct change that fixes the problem, resisting every incidental refactor.
  Use when fixing bugs with the smallest surgical change, avoiding refactors.
---

# Minimal Diff

Make the smallest correct change, and resist everything else.

## Process
1. **Find the root cause before editing.** The lazy fix and the correct fix are the same fix when you know where the problem actually is — a guard in the shared function beats a guard in every caller.
2. **Grep every caller** of anything you are about to change. A change that fixes the reported path and leaves three sibling paths broken is not minimal, it is incomplete.
3. **Change only what the fix requires.** Reformatting, renaming and reordering in the same diff hide the actual change from review.
4. **Do not add abstraction for a single case.** One implementation does not need an interface.
5. **Leave the smallest check that would fail** if the logic breaks — usually one test, not a suite.
6. **Note deliberate shortcuts** with the ceiling and the upgrade path, so a knowing trade-off is not mistaken later for an oversight.

## Deliverables
- Root cause statement, not a symptom description
- The diff, with unrelated changes excluded
- One test that fails without the fix

## Verification & Quality Checklist

- [ ] Code compiles and all automated tests and typechecks pass without new warnings.
- [ ] Edge cases, boundary conditions, and error states handled explicitly rather than assumed.
- [ ] No hardcoded secrets, credentials, or insecure defaults introduced.
- [ ] Changes are covered by a test that fails without them.

## Anti-Patterns & Constraints

- NEVER weaken or skip a failing test to make a change land.
- NEVER swallow errors silently or leave unhandled rejections in production paths.
- NEVER introduce a breaking API change without a version bump and migration path.
